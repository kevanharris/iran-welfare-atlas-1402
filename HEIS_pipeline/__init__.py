"""
HEIS to Parquet Pipeline
Converts Iranian HEIS microdata to Parquet format using HBSIR package
"""

from .convert import (
    setup_hbsir,
    load_table_for_year,
    write_parquet,
    process_table,
    process_all_tables,
)

__version__ = "0.1.0"

__all__ = [
    "setup_hbsir",
    "load_table_for_year",
    "write_parquet",
    "process_table",
    "process_all_tables",
]
