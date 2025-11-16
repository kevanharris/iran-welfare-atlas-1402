# HEIS Parquet Conversion - Documentation

## Overview

This project uses **HBSIR** (Household Budget Survey of Iran - R package) to download and convert Iranian HEIS microdata to Parquet format for offline analysis.

**HBSIR**: Python package by Iran Open Data project that provides cleaned, harmonized HEIS microdata
**Source**: https://github.com/Iran-Open-Data/HBSIR
**Documentation**: https://iran-open-data.github.io/HBSIR/

## Data Coverage Summary

### Years 1387-1403 (2008-2024): COMPLETE
- All 19 tables available in normalized Parquet format
- Includes household_information, members_properties, all expenditure/income tables
- **Location**: `/05_Data/Iran Primary Data/Household Budget Surveys/1375-1403_parquet/`
- **Files**: 492 Parquet files (369MB total)

### Years 1390-1403: Includes subsidy table
- subsidy table only available from year 1390 onward

### Years 1375-1386 (1996-2007): PARTIAL
- **Missing**: household_information table
- **Available**: All other tables (members_properties, expenditures, income)
- **Reason**: See "Why household_information is Missing" section below

## Why household_information is Missing for Years 1375-1386

### The Problem

HBSIR cannot load `household_information` for years 1375-1386 - returns error:
```
ValueError: No objects to concatenate
```

### Root Cause: Data Structure Incompatibility

**Early years (1375-1386)** use a completely different raw data structure:
- Data split into **separate Rural and Urban tables**
- Generic column names (COL01, COL02, etc.) instead of descriptive names
- Different table naming: R75P1, U75P1 (rural/urban household info)

**Example from year 1375 MDB file:**
```
R75P1  - Rural household information
U75P1  - Urban household information
R75P2  - Rural member properties
U75P2  - Urban member properties
R75P3S01-S09 - Rural expenditure sections
U75P3S01-S09 - Urban expenditure sections
R75P4S1-S3 - Rural income sections
U75P4S1-S3 - Urban income sections
```

**Later years (1387+)** use unified structure:
- Single combined table (not split by rural/urban)
- Descriptive column names
- Standardized across years

### What HBSIR Does

HBSIR creates three data "forms":
1. **raw** - Original survey data without modifications
2. **cleaned** - Added labels and types, removed irrelevant values
3. **normalized** - Unified column names, combined rural/urban, standardized across years

**The issue**: HBSIR has only successfully normalized years 1387-1403. For years 1375-1386, the normalization process fails because the underlying raw data structure is incompatible.

### Your Raw Data

You have the original raw data for years 1375-1397 in:
- **Location**: `/05_Data/Iran Primary Data/Household Budget Surveys/1363-1397_mdb-xlsx/`
- **Format**: MDB database files (one per year)
- **Structure**: Rural/urban split tables with generic column names
- **Coverage**: Years 1363-1397

The data EXISTS, but:
- It's in the old rural/urban split format
- Column names are generic (need mapping to variable names)
- Would require custom conversion script to match HBSIR's normalized format

## Data Tables Available

### General Tables
- `household_information` - Household demographics and characteristics (years 1387-1403 only)
- `members_properties` - Individual household member data (all years)

### Expenditure Tables (13 categories)
- `food`, `tobacco`, `cloth`, `home`, `furniture`, `medical`
- `transportation`, `communication`, `entertainment`, `education`
- `hotel`, `miscellaneous`, `durable`

### Income Tables
- `employment_income` - Wage/salary income
- `self_employed_income` - Self-employment income
- `other_income` - Other income sources
- `subsidy` - Subsidy payments (years 1390-1403 only)

## File Organization

### Primary Data Location
```
/05_Data/Iran Primary Data/Household Budget Surveys/
├── 1363-1397_mdb-xlsx/              # Raw MDB files (original SCI data)
│   ├── year_1363/
│   ├── year_1364/
│   ├── ...
│   ├── year_1397/
│   └── Household_Expenditure_Income_Survey_Variables_1363-1398.xlsx
│
└── 1375-1403_parquet/               # HBSIR cleaned Parquet files
    ├── heis_1387_household_information.parquet
    ├── heis_1387_members_properties.parquet
    ├── heis_1387_food.parquet
    └── ... (492 files total)
```

### This Project Folder
```
2025_12_welfare_atlas/
├── CLAUDE.md                        # Project documentation
├── PROJECT_STATE.md                 # Work tracking
├── HEIS_PARQUET_README.md          # This file
├── data/                            # Welfare atlas 1402 data only
│   ├── welfare_atlas_1402.csv
│   └── welfare_atlas_1402.parquet
├── docs/                            # Provincial reports
├── scripts/                         # R analysis scripts
└── output/                          # Analysis outputs
```

**Note**: heis_1395-1398 raw data folders were removed - redundant with HBSIR parquet files.

## Using the Data

### Load HBSIR Parquet Files in R

```r
library(arrow)

# Load household information for year 1400
hh_1400 <- read_parquet(
  "/05_Data/Iran Primary Data/Household Budget Surveys/1375-1403_parquet/heis_1400_household_information.parquet"
)

# Load food expenditures for year 1400
food_1400 <- read_parquet(
  "/05_Data/Iran Primary Data/Household Budget Surveys/1375-1403_parquet/heis_1400_food.parquet"
)

# Load multiple years
years <- 1395:1403
hh_data <- lapply(years, function(year) {
  read_parquet(sprintf(
    "/05_Data/Iran Primary Data/Household Budget Surveys/1375-1403_parquet/heis_%d_household_information.parquet",
    year
  ))
}) %>% bind_rows()
```

### Load HBSIR Parquet Files in Python

```python
import pandas as pd
import pyarrow.parquet as pq

# Load household information for year 1400
hh_1400 = pd.read_parquet(
    "/05_Data/Iran Primary Data/Household Budget Surveys/1375-1403_parquet/heis_1400_household_information.parquet"
)

# Load multiple years
years = range(1395, 1404)
hh_data = pd.concat([
    pd.read_parquet(
        f"/05_Data/Iran Primary Data/Household Budget Surveys/1375-1403_parquet/heis_{year}_household_information.parquet"
    )
    for year in years
], ignore_index=True)
```

## Re-running the Conversion Pipeline

The conversion has already been run and files are stored in the primary data folder. You do NOT need to re-run unless:
- New HBSIR data becomes available
- You want to update existing files
- You need different years or tables

### Prerequisites

```bash
pip install -r requirements.txt
```

**Requirements:**
- hbsir>=0.6.4
- lfsir>=0.6.0 (for Labor Force Survey)
- pandas>=2.0.0
- pyarrow>=10.0.0
- pyyaml>=6.0
- tqdm>=4.65.0

### Configuration

Edit `config.yaml` to specify:
- Output directory
- Year range (1375-1403)
- Tables to download
- Processing options (compression, weights, etc.)

### Run Conversion

```bash
# Activate virtual environment (if using one)
source /tmp/hbsir_env/bin/activate

# Run conversion (from this project directory)
python3 heis_to_parquet.py

# Or for specific years
python3 heis_to_parquet.py --years 1400 1403

# Or for specific table
python3 heis_to_parquet.py --table household_information

# Force reprocess existing files
python3 heis_to_parquet.py --force
```

## Known Limitations

### Missing household_information (Years 1375-1386)
- **Impact**: Cannot link household characteristics to expenditure/income data for these years
- **Workaround**: Use members_properties table for some demographic info, or process raw MDB files manually
- **Alternative**: Start analysis from year 1387

### Missing subsidy table (Years 1375-1389)
- **Impact**: No subsidy/transfer payment data before 1390
- **Reason**: Subsidy table not available in source data for early years

### Data Quality Notes
- All data comes from HBSIR's cleaned repository
- HBSIR may have removed or corrected some values from raw SCI data
- Sampling weights included in household_information (when available)
- See HBSIR documentation for details on cleaning procedures

## Options for Years 1375-1386 household_information

If you need household_information for years 1375-1386, you have three options:

### Option 1: Start Analysis from Year 1387 (Recommended)
- Use HBSIR data from 1387-1403 (17 years of complete data)
- Simplest approach, already available in Parquet format
- Consistent data structure across all years

### Option 2: Use members_properties Instead
- members_properties is available for all years including 1375-1386
- Contains individual-level demographic data
- Can aggregate to household level for some analyses
- Missing household-level characteristics (housing, location, etc.)

### Option 3: Convert Raw MDB Files (Advanced)
- Write custom script to extract and combine R##P1 and U##P1 tables
- Map generic column names (COL01, COL02) to variable names
- Merge rural and urban data
- Standardize to match HBSIR format
- Requires understanding of SCI's codebook and data structure

**Recommendation**: Unless you specifically need years 1375-1386, use Option 1 and start from year 1387.

## Related Resources

### HBSIR Documentation
- **Website**: https://iran-open-data.github.io/HBSIR/
- **GitHub**: https://github.com/Iran-Open-Data/HBSIR
- **Tables Reference**: https://iran-open-data.github.io/HBSIR/tables/

### Variable Documentation
- Student's variable tracking spreadsheet: `1363-1397_mdb-xlsx/Household_Expenditure_Income_Survey_Variables_1363-1398.xlsx`
- Color-coded tracking of schema changes across years 1363-1398
- Useful for understanding raw data evolution

### Labor Force Survey (LFS)
- Similar pipeline for LFSIR (Labor Force Survey)
- Data location: `/05_Data/Iran Primary Data/Labor Force Surveys/parquet/`
- Years 1385-1403 available (19 files, 240MB)
- Single "data" table (101 variables)

## Session Notes

### 2025-11-15: HEIS/LFS Parquet Conversion

**Completed:**
- ✓ Downloaded and converted HEIS data (years 1387-1403, 18 tables, 492 files)
- ✓ Downloaded and converted LFS data (years 1385-1403, 19 files)
- ✓ Investigated missing household_information for years 1375-1386
- ✓ Identified rural/urban split as root cause
- ✓ Confirmed raw data exists in MDB files
- ✓ Documented data structure and limitations

**Key Finding:**
HBSIR has not normalized household_information for years 1375-1386 due to incompatible raw data structure (rural/urban split with generic column names). Data exists but requires custom conversion.

**Files Removed:**
- heis_1395/, heis_1396/, heis_1397/, heis_1398/ - Redundant with HBSIR parquet files
- HBSIR/ and LFSIR/ duplicate folders from data/ directory (609MB)
- Pipeline files (config.yaml, requirements.txt, etc.) - Kept for documentation

**Recommendation:**
Use HBSIR data starting from year 1387 for analyses requiring household_information. For years 1375-1386, either use members_properties or consider custom MDB conversion if household characteristics are critical.
