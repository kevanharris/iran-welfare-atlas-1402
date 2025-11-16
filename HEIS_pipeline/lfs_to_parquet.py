#!/usr/bin/env python3
"""
LFS to Parquet Conversion Script

Downloads Iranian Labor Force Survey microdata using LFSIR and converts
to Parquet format for local storage and offline analysis.

Usage:
    # Process all years from config_lfs.yaml
    python lfs_to_parquet.py

    # Process specific years
    python lfs_to_parquet.py --years 1400 1403

    # Force reprocess existing files
    python lfs_to_parquet.py --force
"""

import argparse
import sys
import logging
from pathlib import Path
import yaml
from tqdm import tqdm
import pandas as pd
import lfsir

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config_lfs.yaml") -> dict:
    """Load configuration from YAML file"""
    config_file = Path(config_path)

    if not config_file.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    logger.info(f"Loaded configuration from {config_path}")
    return config


def setup_lfsir(cache_dir: str) -> None:
    """Configure LFSIR"""
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    try:
        lfsir.setup_config()
    except:
        pass

    logger.info(f"LFSIR initialized (cache directory: {cache_path})")


def process_year(
    year: int,
    out_dir: Path,
    compression: str = 'snappy',
    skip_existing: bool = True
) -> bool:
    """
    Process one year of LFS data

    Parameters
    ----------
    year : int
        Persian calendar year
    out_dir : Path
        Output directory
    compression : str
        Compression algorithm
    skip_existing : bool
        Skip if file exists

    Returns
    -------
    bool
        True if processed, False if skipped or error
    """
    # Check if file exists
    out_dir = Path(out_dir)
    filename = f"lfs_{year}.parquet"
    filepath = out_dir / filename

    if skip_existing and filepath.exists():
        logger.info(f"Skipping year {year} (already exists)")
        return False

    try:
        # Load data
        logger.info(f"Loading LFS data for year {year}")
        df = lfsir.load_table("data", year, on_missing='download')

        # Ensure Year column exists
        if 'Year' not in df.columns:
            df['Year'] = year

        logger.info(f"  Loaded {len(df):,} records")

        # Create output directory if needed
        out_dir.mkdir(parents=True, exist_ok=True)

        # Write to Parquet
        df.to_parquet(
            filepath,
            index=False,
            compression=compression,
            engine='pyarrow'
        )

        # Log file size
        size_mb = filepath.stat().st_size / (1024 * 1024)
        logger.info(f"  Written to {filepath.name} ({size_mb:.1f} MB)")

        return True

    except Exception as e:
        logger.error(f"Error processing year {year}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert LFS microdata to Parquet format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--config',
        default='config_lfs.yaml',
        help='Path to configuration file (default: config_lfs.yaml)'
    )

    parser.add_argument(
        '--years',
        nargs=2,
        type=int,
        metavar=('START', 'END'),
        help='Year range to process (overrides config), e.g., --years 1400 1403'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Reprocess files even if they already exist'
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

    # Determine output directory
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = Path(config['parquet_out_dir'])

    # Get options
    options = config.get('options', {})
    cache_dir = config.get('lfsir_cache_dir', '/tmp/lfsir_cache')
    compression = options.get('compression', 'snappy')
    skip_existing = not args.force and options.get('skip_existing', True)
    show_progress = not args.no_progress and options.get('show_progress', True)

    # Print summary
    print("\n" + "="*70)
    print("LFS TO PARQUET CONVERSION")
    print("="*70)
    print(f"Years: {year_start}-{year_end} ({len(years)} years)")
    print(f"Output directory: {out_dir}")
    print(f"Cache directory: {cache_dir}")
    print(f"Skip existing: {skip_existing}")
    print(f"Compression: {compression}")
    print("="*70 + "\n")

    # Confirm
    response = input("Proceed with conversion? (y/n): ")
    if response.lower() != 'y':
        print("Aborted")
        return 0

    # Setup LFSIR
    logger.info("Setting up LFSIR...")
    setup_lfsir(cache_dir)

    # Process all years
    processed = 0
    skipped = 0
    errors = 0

    iterator = tqdm(years, desc="Processing LFS data") if show_progress else years

    for year in iterator:
        if show_progress:
            iterator.set_description(f"Processing year {year}")

        result = process_year(year, out_dir, compression, skip_existing)

        if result is True:
            processed += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1

    # Summary
    print("\n" + "="*70)
    print("CONVERSION COMPLETE")
    print("="*70)
    print(f"Output directory: {out_dir}")
    print(f"Successfully processed: {processed} files")
    print(f"Skipped (existing): {skipped} files")
    print(f"Errors: {errors} files")
    print("="*70 + "\n")

    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
