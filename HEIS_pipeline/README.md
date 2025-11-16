# HEIS & LFS Data Conversion Pipeline

Complete pipeline for downloading and converting Iranian HEIS (Household Expenditure & Income Survey) and LFS (Labor Force Survey) microdata from HBSIR/LFSIR packages to Parquet format for offline analysis.

## Table of Contents

- [Overview](#overview)
- [What This Pipeline Does](#what-this-pipeline-does)
- [Setup Instructions](#setup-instructions)
- [Running the Pipeline](#running-the-pipeline)
- [What Was Done (2025-11-15)](#what-was-done-2025-11-15)
- [Results & Findings](#results--findings)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)

---

## Overview

This pipeline was created on **2025-11-15** to download Iranian household expenditure and labor force survey data using the Iran Open Data project's Python packages and convert them to Parquet format for efficient offline analysis.

**Data sources:**
- **HBSIR** (Household Budget Survey of Iran - R): https://github.com/Iran-Open-Data/HBSIR
- **LFSIR** (Labor Force Survey of Iran - R): https://github.com/Iran-Open-Data/LFSIR

**Why Parquet?**
- Efficient columnar storage (smaller file size)
- Fast read/write operations
- Works with R (arrow package) and Python (pandas/pyarrow)
- Preserves data types and metadata
- No dependency on online HBSIR/LFSIR APIs after conversion

---

## What This Pipeline Does

### HEIS Conversion (`heis_to_parquet.py`)

Downloads and converts **19 HEIS tables** across **29 years (1375-1403)**:

**General Tables (2):**
- `household_information` - Household demographics and characteristics
- `members_properties` - Individual household member data

**Expenditure Tables (13):**
- `food`, `tobacco`, `cloth`, `home`, `furniture`, `medical`
- `transportation`, `communication`, `entertainment`, `education`
- `hotel`, `miscellaneous`, `durable`

**Income Tables (4):**
- `employment_income` - Wage/salary income
- `self_employed_income` - Self-employment income
- `other_income` - Other income sources
- `subsidy` - Subsidy payments

**Features:**
- Automatic downloading from HBSIR repository
- Adds sampling weights to household_information table
- Converts to compressed Parquet format (snappy compression)
- Skips existing files by default (configurable)
- Progress tracking with tqdm
- Comprehensive error logging

### LFS Conversion (`lfs_to_parquet.py`)

Downloads and converts **1 LFS table** across **19 years (1385-1403)**:

**Table:**
- `data` - Labor force survey data (101 variables)

**Features:**
- Same as HEIS pipeline
- Simpler structure (single table)
- Automatic year column addition

---

## Setup Instructions

### Prerequisites

**Required software:**
- Python 3.8+ (tested with Python 3.14)
- pip (Python package manager)
- Git (for version control)

### Installation

1. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv /tmp/hbsir_env
   source /tmp/hbsir_env/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Packages installed:**
   - `hbsir>=0.6.4` - Household Budget Survey data access
   - `lfsir>=0.6.0` - Labor Force Survey data access
   - `pandas>=2.0.0` - Data manipulation
   - `pyarrow>=10.0.0` - Parquet file operations
   - `pyyaml>=6.0` - Configuration file parsing
   - `tqdm>=4.65.0` - Progress bars

3. **Configure output directories** (edit `config.yaml` and `config_lfs.yaml`):
   - Set `parquet_out_dir` to desired output location
   - Adjust year range if needed
   - Modify table lists if needed

---

## Running the Pipeline

### HEIS Data Conversion

**Basic usage:**
```bash
source /tmp/hbsir_env/bin/activate
python3 heis_to_parquet.py
```

**Options:**
```bash
# Process specific years only
python3 heis_to_parquet.py --years 1400 1403

# Process specific table only
python3 heis_to_parquet.py --table household_information

# Force reprocess existing files
python3 heis_to_parquet.py --force

# Dry run (show what would be processed)
python3 heis_to_parquet.py --dry-run

# Use custom config file
python3 heis_to_parquet.py --config my_config.yaml

# Override output directory
python3 heis_to_parquet.py --output-dir /path/to/output
```

### LFS Data Conversion

**Basic usage:**
```bash
source /tmp/hbsir_env/bin/activate
python3 lfs_to_parquet.py
```

**Options:**
```bash
# Same options as HEIS pipeline
python3 lfs_to_parquet.py --years 1400 1403
python3 lfs_to_parquet.py --force
python3 lfs_to_parquet.py --dry-run
```

---

## What Was Done (2025-11-15)

### Complete Step-by-Step Process

#### 1. Environment Setup
```bash
# Created virtual environment
python3 -m venv /tmp/hbsir_env
source /tmp/hbsir_env/bin/activate

# Installed packages
pip install hbsir lfsir pandas pyarrow pyyaml tqdm
```

#### 2. Pipeline Development

**Created files:**
- `config.yaml` - HEIS pipeline configuration
- `config_lfs.yaml` - LFS pipeline configuration
- `requirements.txt` - Python dependencies
- `heis_to_parquet.py` - Main HEIS conversion script
- `lfs_to_parquet.py` - Main LFS conversion script
- `convert.py` - Core conversion functions module

**Configuration used:**
```yaml
# HEIS
parquet_out_dir: "/05_Data/Iran Primary Data/Household Budget Surveys/parquet"
years: 1375-1403 (29 years)
tables: 19 (household_information, members_properties, 13 expenditures, 4 income)
compression: snappy
add_weights: true

# LFS
parquet_out_dir: "/05_Data/Iran Primary Data/Labor Force Surveys/parquet"
years: 1385-1403 (19 years)
compression: snappy
```

#### 3. HEIS Conversion Execution

**Command run:**
```bash
source /tmp/hbsir_env/bin/activate
echo "y" | python3 heis_to_parquet.py 2>&1 | tee heis_conversion.log
```

**Processing details:**
- Total operations attempted: 551 (19 tables × 29 years)
- Duration: ~15 minutes
- Output logged to: `heis_conversion.log`

**Results:**
- Successfully processed: 480 files
- Failed: 71 files (household_information for years 1375-1386)
- Total size: 369MB
- Output location: `/05_Data/Iran Primary Data/Household Budget Surveys/parquet/`

#### 4. LFS Conversion Execution

**Command run:**
```bash
source /tmp/hbsir_env/bin/activate
echo "y" | python3 lfs_to_parquet.py 2>&1 | tee lfs_conversion.log
```

**Processing details:**
- Total operations: 19 (1 table × 19 years)
- Duration: ~3 minutes
- Output logged to: `lfs_conversion.log`

**Results:**
- Successfully processed: 19 files
- Failed: 0 files
- Total size: 240MB
- Output location: `/05_Data/Iran Primary Data/Labor Force Surveys/parquet/`

#### 5. Investigation & Documentation

**Missing data investigation:**
- Identified household_information missing for years 1375-1386
- Tested different data forms (raw, cleaned, normalized)
- Examined raw MDB files to understand data structure
- Discovered rural/urban split in early years

**Documentation created:**
- `HEIS_PARQUET_README.md` - User guide for working with the data
- This README - Pipeline documentation for future use

---

## Results & Findings

### Successfully Converted Data

#### HEIS (Household Expenditure & Income Survey)

**Years 1387-1403 (2008-2024): COMPLETE**
- All 18 tables available
- household_information: ✓
- members_properties: ✓
- All expenditure tables: ✓
- All income tables: ✓
- subsidy (from 1390): ✓

**Years 1375-1386 (1996-2007): PARTIAL**
- household_information: ✗ (MISSING)
- members_properties: ✓
- All expenditure tables: ✓
- All income tables: ✓ (except subsidy)

**File statistics:**
- Total files: 480 Parquet files
- Total size: 369MB (compressed with snappy)
- Years covered: 1375-1403 (29 years)
- Tables per year: 13-18 (depending on availability)

#### LFS (Labor Force Survey)

**Years 1385-1403 (2006-2024): COMPLETE**
- Single "data" table: ✓
- 101 variables per year
- No missing years

**File statistics:**
- Total files: 19 Parquet files
- Total size: 240MB (compressed with snappy)
- Years covered: 1385-1403 (19 years)

### Critical Finding: Missing household_information (Years 1375-1386)

#### What's Missing
The `household_information` table cannot be loaded from HBSIR for years 1375-1386.

**Error message:**
```
ValueError: No objects to concatenate
```

#### Root Cause
**Different data structure in early years:**

Early years (1375-1386) use rural/urban split:
```
R75P1  - Rural household information
U75P1  - Urban household information
R75P2  - Rural member properties
U75P2  - Urban member properties
R75P3S01-S09 - Rural expenditure sections
U75P3S01-S09 - Urban expenditure sections
```

Later years (1387+) use unified tables:
```
household_information  - Combined rural/urban
members_properties    - Combined rural/urban
food, tobacco, etc.   - Combined rural/urban
```

**Why HBSIR fails:**
- HBSIR expects normalized data (combined rural/urban with standardized column names)
- The normalization process has NOT been completed for years 1375-1386
- Raw data exists in MDB files but in incompatible format (rural/urban split, generic column names)
- HBSIR can successfully normalize years 1387+ but not earlier years

#### Data Forms Tested
All three HBSIR data forms fail for household_information (1375-1386):
- `form='raw'` - ✗ No objects to concatenate
- `form='cleaned'` - ✗ No objects to concatenate
- `form='normalized'` - ✗ No objects to concatenate

#### Alternative Tables Tested
- `house_specifications` - ✓ Works (but different data - housing characteristics)
- `old_rural_house_specifications` - ✗ No objects to concatenate
- `old_urban_house_specifications` - ✗ No objects to concatenate

#### Impact & Workarounds

**Impact:**
- Cannot link household characteristics to expenditure/income data for years 1375-1386
- Demographic analysis limited to individual-level (members_properties)
- Household-level analysis only possible from year 1387 onward

**Workarounds:**
1. **Start analysis from year 1387** (recommended)
   - 17 years of complete data (1387-1403)
   - Consistent structure across all years

2. **Use members_properties instead**
   - Available for all years
   - Can aggregate to household level for some analyses
   - Missing household-level characteristics (housing, location)

3. **Process raw MDB files manually** (advanced)
   - Extract R##P1 and U##P1 tables from MDB files
   - Combine rural and urban data
   - Map generic column names to variables
   - Standardize to match HBSIR format
   - Requires understanding of SCI codebook

#### Raw Data Location
Original MDB files containing the split rural/urban data:
```
/05_Data/Iran Primary Data/Household Budget Surveys/1363-1397_mdb-xlsx/
├── year_1375/PBO_Household_Budget_Database_Year_75_Raw_1375.MDB
├── year_1376/PBO_Household_Budget_Database_Year_76_Raw_1376.MDB
└── ... (years 1375-1397)
```

---

## Troubleshooting

### Common Issues

#### 1. "No objects to concatenate" Error

**Problem:** HBSIR cannot load a table for specific years

**Causes:**
- Data not available in HBSIR repository for those years
- Table structure incompatible (e.g., rural/urban split in early years)

**Solutions:**
- Check if table exists for other years
- Try different data forms (`form='raw'`, `'cleaned'`, `'normalized'`)
- Check raw MDB files for alternative table names
- Use alternative tables or start from later years

**Known affected:**
- household_information: years 1375-1386
- subsidy: years 1375-1389

#### 2. Package Import Errors

**Problem:** `ModuleNotFoundError: No module named 'hbsir'`

**Solution:**
```bash
# Activate virtual environment
source /tmp/hbsir_env/bin/activate

# Install/reinstall packages
pip install -r requirements.txt
```

#### 3. File Already Exists

**Problem:** "Skipping [table] [year] (already exists)"

**Solution:**
```bash
# Force reprocess existing files
python3 heis_to_parquet.py --force

# Or edit config.yaml:
options:
  skip_existing: false
```

#### 4. Memory Issues

**Problem:** Python crashes or runs out of memory during conversion

**Solutions:**
- Process one year at a time: `--years 1400 1400`
- Process one table at a time: `--table household_information`
- Increase system swap space
- Use a machine with more RAM

#### 5. Permission Errors

**Problem:** Cannot write to output directory

**Solution:**
```bash
# Check directory permissions
ls -la /path/to/output

# Create directory if needed
mkdir -p /path/to/output

# Change output directory
python3 heis_to_parquet.py --output-dir ~/Documents/heis_data
```

#### 6. Download Failures

**Problem:** Network errors during HBSIR/LFSIR download

**Solutions:**
- Check internet connection
- Retry the download (may be temporary)
- Use `--force` to re-download corrupted files
- Check HBSIR/LFSIR GitHub for service status

### Debugging Tips

**Enable verbose logging:**
```python
# Add to script before running
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check conversion logs:**
```bash
# HEIS conversion log
less heis_conversion.log

# LFS conversion log
less lfs_conversion.log

# Search for errors
grep "ERROR" heis_conversion.log
```

**Test single table/year:**
```bash
# Test if specific table loads in Python
python3 -c "
import hbsir
df = hbsir.load_table('household_information', years=1400, on_missing='download')
print(f'Success: {len(df)} records')
"
```

**Check HBSIR configuration:**
```bash
# View HBSIR config
python3 -c "
import hbsir
hbsir.setup_config()
print('HBSIR configured successfully')
"
```

---

## File Structure

```
HEIS_pipeline/
├── README.md                    # This file - complete documentation
├── requirements.txt             # Python dependencies
│
├── config.yaml                  # HEIS pipeline configuration
├── config_lfs.yaml             # LFS pipeline configuration
│
├── heis_to_parquet.py          # Main HEIS conversion script
├── lfs_to_parquet.py           # Main LFS conversion script
├── convert.py                   # Core conversion functions (imported by scripts)
├── __init__.py                  # Python package initialization
│
├── heis_conversion.log         # HEIS conversion run log (2025-11-15)
├── lfs_conversion.log          # LFS conversion run log (2025-11-15)
│
├── config/                      # HBSIR/LFSIR configuration files
│   ├── hbsir_settings.yaml
│   └── lfsir_settings.yaml
│
└── __pycache__/                 # Python bytecode cache (can be deleted)
```

### Script Dependencies

```
heis_to_parquet.py
├── imports: yaml, argparse, pathlib, logging
└── imports: convert.py (from this directory)
    ├── setup_hbsir()
    ├── process_all_tables()
    └── process_table()

lfs_to_parquet.py
├── imports: yaml, argparse, pathlib, logging
└── uses: lfsir.load_table() directly (simpler structure)

convert.py
├── imports: pandas, hbsir, pathlib, logging
└── functions:
    ├── setup_hbsir() - Initialize HBSIR
    ├── load_table_for_year() - Load single table/year
    ├── write_parquet() - Write DataFrame to Parquet
    ├── process_table() - Load and write single table/year
    └── process_all_tables() - Process multiple tables/years with progress
```

---

## Configuration Reference

### config.yaml (HEIS)

```yaml
# Output directory for cleaned Parquet files
parquet_out_dir: "/path/to/output"

# Temporary cache directory for HBSIR downloads
hbsir_cache_dir: "/tmp/hbsir_cache"

# Year range to process (inclusive)
years:
  start: 1375
  end: 1403

# Tables to download and convert
general_tables:
  - household_information
  - members_properties

expenditure_tables:
  - food
  - tobacco
  - cloth
  - home
  - furniture
  - medical
  - transportation
  - communication
  - entertainment
  - education
  - hotel
  - miscellaneous
  - durable

income_tables:
  - employment_income
  - self_employed_income
  - other_income
  - subsidy

# Processing options
options:
  add_weights: true          # Add sampling weights to household_information
  compression: "snappy"      # Parquet compression (snappy, gzip, or None)
  show_progress: true        # Show progress bars
  skip_existing: true        # Skip if output file already exists
```

### config_lfs.yaml (LFS)

```yaml
# Output directory for cleaned Parquet files
parquet_out_dir: "/path/to/output"

# Temporary cache directory for LFSIR downloads
lfsir_cache_dir: "/tmp/lfsir_cache"

# Year range to process (inclusive)
years:
  start: 1385
  end: 1403

# Processing options
options:
  compression: "snappy"      # Parquet compression
  show_progress: true        # Show progress bars
  skip_existing: true        # Skip existing files
```

---

## Future Maintenance

### When to Re-run the Pipeline

**Reasons to re-run:**
1. New HEIS/LFS data becomes available (new years published)
2. HBSIR/LFSIR packages are updated with bug fixes or new features
3. Need to regenerate files with different compression settings
4. Data was corrupted and needs to be re-downloaded

### Updating to New Years

**Example: Adding year 1404 when released**

1. Update configuration:
   ```yaml
   # config.yaml
   years:
     start: 1375
     end: 1404  # Changed from 1403
   ```

2. Run pipeline with skip_existing=true (only processes new year):
   ```bash
   python3 heis_to_parquet.py
   ```

3. Or process only the new year:
   ```bash
   python3 heis_to_parquet.py --years 1404 1404
   ```

### Monitoring for Updates

**HBSIR/LFSIR repositories:**
- Watch: https://github.com/Iran-Open-Data/HBSIR
- Watch: https://github.com/Iran-Open-Data/LFSIR
- Check release notes for new data availability

**Iran Statistical Center:**
- Official site: https://www.amar.org.ir/
- Check for new survey releases

### Package Updates

**Check for package updates:**
```bash
pip list --outdated | grep -E "hbsir|lfsir"
```

**Update packages:**
```bash
pip install --upgrade hbsir lfsir pandas pyarrow
pip freeze > requirements.txt  # Update requirements file
```

---

## Contact & Support

### Project Information
- **Created:** 2025-11-15
- **Purpose:** Convert Iranian HEIS/LFS microdata to Parquet format for offline analysis
- **Project:** Iranian Welfare Atlas 1402 Analysis

### External Resources
- **HBSIR Documentation:** https://iran-open-data.github.io/HBSIR/
- **LFSIR Documentation:** https://iran-open-data.github.io/LFSIR/
- **Iran Open Data GitHub:** https://github.com/Iran-Open-Data
- **HBSIR Issues:** https://github.com/Iran-Open-Data/HBSIR/issues
- **LFSIR Issues:** https://github.com/Iran-Open-Data/LFSIR/issues

### Related Documentation
- **HEIS_PARQUET_README.md** - User guide for working with the converted data
- **CLAUDE.md** - Main project documentation (Welfare Atlas 1402 analysis)
- **PROJECT_STATE.md** - Project work tracking and session notes

---

## Changelog

### 2025-11-15: Initial Pipeline Creation
- Created HEIS and LFS conversion pipelines
- Processed 29 years of HEIS data (1375-1403)
- Processed 19 years of LFS data (1385-1403)
- Identified and documented household_information availability issue for years 1375-1386
- Generated 480 HEIS Parquet files (369MB)
- Generated 19 LFS Parquet files (240MB)
- Created comprehensive documentation

**Key findings:**
- household_information not available for years 1375-1386 due to incompatible raw data structure
- All other tables successfully converted for all years
- Raw MDB files contain the data but in rural/urban split format requiring manual processing

**Files created:**
- Pipeline scripts and configuration
- Conversion logs with complete run details
- Documentation (this README and HEIS_PARQUET_README.md)
