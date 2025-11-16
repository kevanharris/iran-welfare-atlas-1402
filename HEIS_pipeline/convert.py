"""
Core conversion functions for HEIS to Parquet pipeline
"""

import logging
from pathlib import Path
from typing import List, Optional
import pandas as pd
import hbsir

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_hbsir(cache_dir: str) -> None:
    """
    Configure HBSIR and create cache directory

    Parameters
    ----------
    cache_dir : str
        Directory for HBSIR to cache downloaded data

    Note
    ----
    HBSIR downloads data to its default location. The cache_dir parameter
    is created for reference but HBSIR manages its own cache internally.
    """
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    # Initialize HBSIR config (creates default settings if needed)
    try:
        hbsir.setup_config()
    except:
        pass  # Config may already exist

    logger.info(f"HBSIR initialized (cache directory: {cache_path})")


def load_table_for_year(
    table_name: str,
    year: int,
    add_weights: bool = False
) -> pd.DataFrame:
    """
    Load a table for a specific year using HBSIR

    Parameters
    ----------
    table_name : str
        Name of the table to load (e.g., 'household_information', 'food')
    year : int
        Persian calendar year (e.g., 1400)
    add_weights : bool, default False
        Whether to add sampling weights (only applicable to household tables)

    Returns
    -------
    pd.DataFrame
        Loaded and cleaned table data
    """
    logger.info(f"Loading {table_name} for year {year}")

    try:
        # Load the table (will download if not cached)
        df = hbsir.load_table(
            table_name,
            years=year,
            on_missing='download'
        )

        # Add weights if requested and applicable
        if add_weights and table_name == 'household_information':
            try:
                df = hbsir.add_weight(df)
                logger.info(f"  Added sampling weights to {table_name}")
            except Exception as e:
                logger.warning(f"  Could not add weights: {e}")

        # Ensure Year column exists
        if 'Year' not in df.columns:
            df['Year'] = year

        logger.info(f"  Loaded {len(df):,} records")
        return df

    except Exception as e:
        logger.error(f"  Error loading {table_name} for year {year}: {e}")
        raise


def write_parquet(
    df: pd.DataFrame,
    table_name: str,
    year: int,
    out_dir: Path,
    compression: str = 'snappy'
) -> Path:
    """
    Write DataFrame to Parquet file with standardized naming

    Parameters
    ----------
    df : pd.DataFrame
        Data to write
    table_name : str
        Name of the table
    year : int
        Persian calendar year
    out_dir : Path
        Output directory
    compression : str, default 'snappy'
        Compression algorithm (snappy, gzip, or None)

    Returns
    -------
    Path
        Path to written file
    """
    # Create output directory if needed
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Standardized filename: heis_YEAR_tablename.parquet
    filename = f"heis_{year}_{table_name}.parquet"
    filepath = out_dir / filename

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

    return filepath


def process_table(
    table_name: str,
    year: int,
    out_dir: Path,
    add_weights: bool = False,
    compression: str = 'snappy',
    skip_existing: bool = True
) -> Optional[Path]:
    """
    Process a single table for a single year: load and write to Parquet

    Parameters
    ----------
    table_name : str
        Name of the table
    year : int
        Persian calendar year
    out_dir : Path
        Output directory
    add_weights : bool, default False
        Whether to add sampling weights
    compression : str, default 'snappy'
        Compression algorithm
    skip_existing : bool, default True
        Skip if output file already exists

    Returns
    -------
    Optional[Path]
        Path to written file, or None if skipped
    """
    # Check if file already exists
    out_dir = Path(out_dir)
    filename = f"heis_{year}_{table_name}.parquet"
    filepath = out_dir / filename

    if skip_existing and filepath.exists():
        logger.info(f"Skipping {table_name} {year} (already exists)")
        return None

    try:
        # Load the table
        df = load_table_for_year(table_name, year, add_weights=add_weights)

        # Write to Parquet
        output_path = write_parquet(
            df, table_name, year, out_dir, compression=compression
        )

        return output_path

    except Exception as e:
        logger.error(f"Failed to process {table_name} for year {year}: {e}")
        return None


def process_all_tables(
    tables: List[str],
    years: List[int],
    out_dir: Path,
    add_weights: bool = False,
    compression: str = 'snappy',
    skip_existing: bool = True,
    show_progress: bool = True
) -> dict:
    """
    Process multiple tables across multiple years

    Parameters
    ----------
    tables : List[str]
        List of table names to process
    years : List[int]
        List of years to process
    out_dir : Path
        Output directory
    add_weights : bool, default False
        Whether to add sampling weights to household tables
    compression : str, default 'snappy'
        Compression algorithm
    skip_existing : bool, default True
        Skip existing files
    show_progress : bool, default True
        Show progress bars

    Returns
    -------
    dict
        Summary statistics of processing
    """
    from tqdm import tqdm

    total_tables = len(tables) * len(years)
    processed = 0
    skipped = 0
    errors = 0

    logger.info(f"Processing {len(tables)} tables across {len(years)} years")
    logger.info(f"Total operations: {total_tables}")

    # Create iterator with optional progress bar
    if show_progress:
        iterator = tqdm(
            [(table, year) for table in tables for year in years],
            desc="Processing HEIS data",
            unit="table"
        )
    else:
        iterator = [(table, year) for table in tables for year in years]

    for table_name, year in iterator:
        if show_progress:
            iterator.set_description(f"Processing {table_name} {year}")

        result = process_table(
            table_name,
            year,
            out_dir,
            add_weights=add_weights,
            compression=compression,
            skip_existing=skip_existing
        )

        if result is None:
            skipped += 1
        elif result:
            processed += 1
        else:
            errors += 1

    # Summary
    summary = {
        'total': total_tables,
        'processed': processed,
        'skipped': skipped,
        'errors': errors
    }

    logger.info("\n" + "="*70)
    logger.info("PROCESSING COMPLETE")
    logger.info(f"Total operations: {total_tables}")
    logger.info(f"Successfully processed: {processed}")
    logger.info(f"Skipped (already exist): {skipped}")
    logger.info(f"Errors: {errors}")
    logger.info("="*70)

    return summary
