#!/usr/bin/env python3
"""
HEIS to Parquet Conversion Script

Downloads Iranian HEIS microdata using HBSIR and converts to Parquet format
for local storage and offline analysis.

Usage:
    # Process all tables and years from config.yaml
    python heis_to_parquet.py

    # Process specific years
    python heis_to_parquet.py --years 1400 1403

    # Process specific table only
    python heis_to_parquet.py --table household_information

    # Force reprocess existing files
    python heis_to_parquet.py --force

    # Dry run (show what would be processed)
    python heis_to_parquet.py --dry-run
"""

import argparse
import sys
from pathlib import Path
import yaml
import logging

from heis_pipeline import (
    setup_hbsir,
    process_all_tables,
    process_table,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    config_file = Path(config_path)

    if not config_file.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    logger.info(f"Loaded configuration from {config_path}")
    return config


def get_all_tables(config: dict) -> list:
    """Get list of all tables from config"""
    tables = []
    tables.extend(config.get('general_tables', []))
    tables.extend(config.get('expenditure_tables', []))
    tables.extend(config.get('income_tables', []))
    return tables


def main():
    parser = argparse.ArgumentParser(
        description='Convert HEIS microdata to Parquet format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--years',
        nargs=2,
        type=int,
        metavar=('START', 'END'),
        help='Year range to process (overrides config), e.g., --years 1400 1403'
    )

    parser.add_argument(
        '--table',
        help='Process only specific table (e.g., household_information)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Reprocess files even if they already exist'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be processed without actually processing'
    )

    parser.add_argument(
        '--output-dir',
        help='Override output directory from config'
    )

    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Disable progress bars'
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Determine year range
    if args.years:
        year_start, year_end = args.years
    else:
        year_start = config['years']['start']
        year_end = config['years']['end']

    years = list(range(year_start, year_end + 1))

    # Determine tables to process
    if args.table:
        tables = [args.table]
    else:
        tables = get_all_tables(config)

    # Determine output directory
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = Path(config['parquet_out_dir'])

    # Get options
    options = config.get('options', {})
    cache_dir = config.get('hbsir_cache_dir', '/tmp/hbsir_cache')
    add_weights = options.get('add_weights', True)
    compression = options.get('compression', 'snappy')
    skip_existing = not args.force and options.get('skip_existing', True)
    show_progress = not args.no_progress and options.get('show_progress', True)

    # Print summary
    print("\n" + "="*70)
    print("HEIS TO PARQUET CONVERSION")
    print("="*70)
    print(f"Years: {year_start}-{year_end} ({len(years)} years)")
    print(f"Tables: {len(tables)}")
    for table in tables:
        print(f"  - {table}")
    print(f"Output directory: {out_dir}")
    print(f"Cache directory: {cache_dir}")
    print(f"Total operations: {len(tables) * len(years)}")
    print(f"Skip existing: {skip_existing}")
    print(f"Add weights: {add_weights}")
    print(f"Compression: {compression}")
    print("="*70 + "\n")

    if args.dry_run:
        print("DRY RUN - No files will be processed")
        return 0

    # Confirm before proceeding
    response = input("Proceed with conversion? (y/n): ")
    if response.lower() != 'y':
        print("Aborted")
        return 0

    # Setup HBSIR
    logger.info("Setting up HBSIR...")
    setup_hbsir(cache_dir)

    # Process all tables
    summary = process_all_tables(
        tables=tables,
        years=years,
        out_dir=out_dir,
        add_weights=add_weights,
        compression=compression,
        skip_existing=skip_existing,
        show_progress=show_progress
    )

    # Final summary
    print("\n" + "="*70)
    print("CONVERSION COMPLETE")
    print("="*70)
    print(f"Output directory: {out_dir}")
    print(f"Successfully processed: {summary['processed']} files")
    print(f"Skipped (existing): {summary['skipped']} files")
    print(f"Errors: {summary['errors']} files")
    print("="*70 + "\n")

    if summary['errors'] > 0:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
