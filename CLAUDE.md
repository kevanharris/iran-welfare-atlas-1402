# Iranian Welfare Atlas 1402 (2023-24) Analysis

## Project Overview

Analysis of 2% sample welfare atlas data (1.7M individuals, ~600K households) from Iranian year 1402 (2023-24).

**Primary goal:** Understand household welfare distribution across Iran and prepare for integration with longitudinal household expenditure/consumption datasets (HEIS).

**Data source:** Statistical Center of Iran welfare atlas
**Timeline:** Data covers years 1395-1402 (2016-2024 Gregorian) with travel data from 1395-1399 (2016-2020) and financial data from 1398-1402 (2019-2024)

### Persian-Gregorian Year Conversion
| Persian Year | Gregorian Period | Notes |
|--------------|------------------|-------|
| 1395 | Mar 20, 2016 - Mar 20, 2017 | Travel data start |
| 1396 | Mar 21, 2017 - Mar 20, 2018 | |
| 1397 | Mar 21, 2018 - Mar 20, 2019 | |
| 1398 | Mar 21, 2019 - Mar 20, 2020 | Financial data start |
| 1399 | Mar 21, 2020 - Mar 20, 2021 | Pandemic period |
| 1400 | Mar 21, 2021 - Mar 20, 2022 | |
| 1401 | Mar 21, 2022 - Mar 20, 2023 | Digital payments start |
| 1402 | Mar 21, 2023 - Mar 19, 2024 | Dataset compilation year |

## Data Structure

### Main Dataset

**File:** `data/welfare_atlas_1402.csv` (338MB)
**Observations:** 1,697,816 individuals
**Variables:** 48 columns
**Encoding:** UTF-8 (Persian text)

### Key Identifiers

- **`id`**: Individual identifier (12-digit unique ID)
- **`Parent_Id`**: Household head identifier (enables household-level analysis)
  - When `id = Parent_Id`, the individual is the household head
  - Multiple individuals share the same `Parent_Id` within households
  - Critical for aggregating to household level

### Variable Categories

#### 1. Demographics (columns 3-7)
- `GenderId`: 1=Male, 2=Female
- `Age`: 0-99 years (integer)
- `ISBimarKhas`: Special illness indicator (mostly missing)
- `IsMalool`: Disability status (mostly missing)
- `Malool_shedat`: Disability severity (mostly missing)

#### 2. Geographic Identifiers (columns 8-11)
- `Dashboard_postalcode7Digits`: 7-digit postal code
- `isurban`: 0=Rural, 1=Urban
- `SabteAhval_provincename`: Province name (Persian text)
- `SabteAhval_countyname`: County name (Persian text)

**Coverage:** 14 provinces identified in sample (قم, خراسان رضوی, یزد, فارس, گیلان, اصفهان, خوزستان, کرمانشاه, آذربایجان غربی, سیستان وبلوچستان, چهارمحال وبختیاری, کهگیلویه وبویراحمد, and others)

**Data quality note:** 141,430 observations (8.3%) have missing province names

#### 3. Welfare Programs (columns 12-15)
- `Has_SoeTaghzie`: Nutrition subsidy recipient
- `IsBehzisti_AfzayeshMostamari`: Behzisti continuous increase program
- `IsKomite_AfzayeshMostamari`: Komite continuous increase program
- `IsKomite_AfzayeshMostamariSayer`: Komite other continuous increase

#### 4. Travel Behavior (columns 16-19)
**Time period:** 1395-1399 (2016-2020 Gregorian)
- `TripCountAirPilgrimage_95to99`: Air pilgrimage trips
- `TripCountAirNonPilgrimage_95to99`: Air non-pilgrimage trips
- `TripCountNonAirPilgrimage_95to99`: Non-air pilgrimage trips
- `TripCountNonAirNonPilgrimage_95to99`: Non-air non-pilgrimage trips

#### 5. Economic Status (columns 20-28)
- `Has_Saham_Edalat`: Justice shares holder
- `Decile`: Wealth decile (1-10)
- `Percentile`: Wealth percentile (0-100)
- `HasMojavezSenfi`: Industrial license holder
- `ISKarmanddolat_1402`: Government employee in 1402 (2023-24)
- `IsRetired_Asli`: Primary retirement status
- `IsRetired_Tabaie`: Dependent retirement status
- `is_bime_darman`: Health insurance coverage
- `IsBimePardaz`: Insurance payer

#### 6. Banking/Financial Data (columns 29-44)
**Time-series across Iranian years 1398-1402 (2019-2024)**
**Units:** All financial variables in Rials

Bank account balances (years 1399-1400):
- `MandehAval_1399/1400`: Beginning balance (Rials)
- `MandehAkhar_1399/1400`: Ending balance (Rials)
- `Variz_1400`: Deposits in 1400 (Rials)

Monthly transaction averages:
- `CardPerMonth_1398/1399/1400/1401/1402`: Monthly card purchases (Rials)
- `CardBeCardPerMonth_1401/1402`: Monthly card-to-card transfers, account circulation (Rials)
- `SatnaPerMonth_1401/1402`: Monthly Satna interbank system transactions, account circulation (Rials)
- `PayaPerMonth_1401/1402`: Monthly Paya payment system transactions, account circulation (Rials)

#### 7. Assets (columns 45-47)
- `CarsPrice`: Total car value (Rials)
- `CarsCount`: Number of cars owned
- `Bourse_NetPortfoValue`: Stock exchange portfolio value (Rials)

#### 8. Income (column 48)
- `Daramad`: Total registered income (Rials) - includes all officially recorded income sources

### Supporting Documentation

**Codebook:** `data/codebook.xlsx` - 48 variables with Persian descriptions and units
**Provincial reports:** 31 PDF files in `docs/` folder (01-WAzar.pdf through 31-Yazd.pdf, 8-14MB each)

## Data Quality Assessment

### Strengths
- Large, comprehensive individual-level dataset
- Persian text encoding working correctly (UTF-8)
- Hierarchical structure enables both individual and household analysis
- Time-series financial data across 5 years (1398-1402)
- Rich set of welfare, economic, and demographic indicators
- Geographic identifiers at province and county level

### Known Issues
1. **Missing geographic data:** 8.3% of observations lack province/county information
2. **Extensive missing values:** Most rows have 20-29 missing values across 48 variables
   - Disability variables mostly empty
   - Financial variables sparse (many zeros and blanks)
   - Some travel variables all zeros
3. **Sample selection unclear:** "nemone_2_darsadi" suggests "2% sample" but of what population?
4. **Provincial coverage:** Only 14 of 31 Iranian provinces appear in sample - need to verify if stratified sampling
5. **Variable year coverage inconsistent:**
   - Travel data: 1395-1399 only
   - Bank balances: 1399-1400 only
   - Card transactions: 1398-1402 (complete series)
   - Digital payments (CardBeCard, Satna, Paya): 1401-1402 only

## Analysis Phases

### Phase 1: Data Preparation & Validation
**Goal:** Clean data and create analysis-ready household dataset

Tasks:
1. ✓ Codebook read - 48 variables verified with Persian descriptions
2. Calculate missing data patterns by variable
3. Verify geographic coverage (which 14 provinces? why not all 31?)
4. Aggregate to household level using `Parent_Id`
5. Create household composition variables (size, age structure, dependency ratio)
6. Document data quality issues and create analysis-ready variable dictionary

**Output:**
- `output/01_data_preparation/household_data.rds`
- `output/01_data_preparation/data_quality_report.html`
- `output/01_data_preparation/variable_dictionary.csv`

### Phase 2: Descriptive Analysis
**Goal:** Understand welfare distribution patterns

Tasks:
1. Wealth distribution (deciles, percentiles, Gini coefficient)
2. Geographic patterns (provincial comparison, urban/rural)
3. Welfare program coverage and overlap analysis
4. Asset ownership distributions (cars, stocks)
5. Financial inclusion metrics (banking access, transaction patterns)
6. Demographic composition (age, gender, household structure)

**Output:**
- `output/02_descriptive/wealth_distribution.png`
- `output/02_descriptive/geographic_maps.png`
- `output/02_descriptive/summary_tables.xlsx`
- `output/02_descriptive/descriptive_report.html`

### Phase 3: Targeting Analysis
**Goal:** Evaluate welfare program targeting effectiveness

Tasks:
1. Welfare program incidence by income decile
2. Leakage analysis (high-income recipients) and coverage gaps (low-income non-recipients)
3. Compare targeting across program types (nutrition subsidy, Behzisti, Komite)
4. Provincial variation in program efficiency
5. Overlap analysis (multiple program participation)

**Output:**
- `output/03_targeting/program_incidence.png`
- `output/03_targeting/targeting_analysis.html`
- `output/03_targeting/leakage_coverage_table.csv`

### Phase 4: Time-Series Analysis
**Goal:** Track financial behavior evolution 2019-2023

Tasks:
1. Banking activity trends across 5 years
2. Pandemic effects on transactions (1398-1400 / 2019-2021)
3. Digital payment adoption patterns (card vs cash, Satna/Paya growth)
4. Bank balance evolution by wealth group
5. Financial inclusion dynamics

**Output:**
- `output/04_timeseries/financial_trends.png`
- `output/04_timeseries/pandemic_analysis.html`
- `output/04_timeseries/digital_payment_adoption.png`

### Phase 5: Longitudinal Preparation
**Goal:** Prepare for integration with HEIS and other consumption datasets

Tasks:
1. Map variables to HEIS (Household Expenditure & Income Survey) structure
2. Create comparable welfare indicators across datasets
3. Identify geographic and demographic crosswalk needs
4. Document methodology for future integration
5. Create baseline welfare measures for trend analysis
6. Identify key consumption/expenditure proxies in current data

**Output:**
- `output/05_longitudinal_prep/variable_mapping.csv`
- `output/05_longitudinal_prep/integration_guide.md`
- `output/05_longitudinal_prep/comparable_indicators.rds`

## Suggested Analyses

### High-Priority Research Questions

1. **Household Welfare Profiling**
   - Aggregate to household level, create comprehensive welfare indices
   - Combine income, assets, financial activity into multidimensional measure
   - Compare household types (size, composition, headship)

2. **Geographic Inequality**
   - Provincial comparison of welfare indicators
   - Urban vs rural disparities in income, assets, banking access
   - County-level analysis where data permits

3. **Welfare Program Targeting**
   - Who receives benefits? Compare recipients vs non-recipients by decile
   - Assess targeting efficiency (leakage and coverage)
   - Program overlap patterns

4. **Financial Behavior Dynamics**
   - Evolution 2019-2023 (captures pandemic period)
   - Digital payment adoption
   - Financial inclusion gaps

5. **Wealth Inequality**
   - Asset distribution (cars, stocks)
   - Relationship between income deciles and asset ownership
   - Asset-based vs income-based welfare measures

6. **Gender & Age Dimensions**
   - Economic outcomes by gender within households
   - Female-headed vs male-headed households
   - Age structure and elderly welfare

## Methodology Notes

### Household Aggregation Strategy
- Use `Parent_Id` to group individuals into households
- Sum: income, assets, financial transactions
- Calculate: household size, dependency ratio (children + elderly / working-age)
- Identify: household head characteristics (age, gender, employment)
- Create: household-level deciles/percentiles

### Weighting Considerations
- Verify if sampling weights available in dataset or documentation
- Understand sampling frame: 2% of what population?
- Check if stratified by province, urban/rural
- Adjust for non-response if documented

### Geographic Analysis
- 31 provinces in Iran total - only 14 appear in sample
- Verify if 2% sample stratified by province
- Use urban/rural split for within-province analysis
- Address missing province data (8.3% of observations)

### Time-Series Approach
- Financial data spans 1398-1402 (2019-2024)
- Travel data limited to 1395-1399 (2016-2020)
- Pandemic period: 1398-1400 (March 2019 - March 2021)
- Consider inflation adjustment for financial variables (all in Rials)
- Note: Different variables have different year coverage (see Known Issues)

## Output Structure

```
output/
├── 01_data_preparation/
│   ├── household_data.rds
│   ├── data_quality_report.html
│   └── variable_dictionary.csv
├── 02_descriptive/
│   ├── wealth_distribution.png
│   ├── geographic_maps.png
│   ├── summary_tables.xlsx
│   └── descriptive_report.html
├── 03_targeting/
│   ├── program_incidence.png
│   ├── targeting_analysis.html
│   └── leakage_coverage_table.csv
├── 04_timeseries/
│   ├── financial_trends.png
│   ├── pandemic_analysis.html
│   └── digital_payment_adoption.png
└── 05_longitudinal_prep/
    ├── variable_mapping.csv
    ├── integration_guide.md
    └── comparable_indicators.rds
```

## Scripts Structure

```
scripts/
├── 01_read_codebook.R
├── 02_create_household_dataset.R
├── 03_data_quality_check.R
├── 10_descriptive_analysis.R
├── 11_geographic_analysis.R
├── 20_targeting_analysis.R
├── 30_timeseries_analysis.R
└── 40_longitudinal_prep.R
```

## Open Questions

**About the data:**
- What population does the 2% sample represent? (all Iran? specific provinces?)
- Are sampling weights provided or documented?
- Why only 14 of 31 provinces? Which provinces are included?
- ✓ Units clarified: All financial variables in Rials
- ✓ Daramad = Total registered income (not limited to one source)
- How to handle missing province data (8.3% of observations)?
- Is Daramad annual or cumulative across years?

**About longitudinal integration:**
- Which HEIS waves available for matching?
- Are there previous welfare atlas rounds (earlier than 1402)?
- What geographic/demographic identifiers needed for matching?
- How to handle different sampling frames across datasets?

## Future Integration Strategy

### Target Datasets for Combination
- **HEIS (Household Expenditure & Income Survey)** - annual waves
- **Previous welfare atlas rounds** (if available)
- **Administrative welfare program data** (if accessible)
- **Census data** for population benchmarking

### Integration Approach
1. Match on geographic identifiers (province, county, urban/rural)
2. Use comparable welfare indicators across datasets
3. Create consistent household definitions
4. Document any sampling/coverage differences
5. Consider temporal alignment (Persian vs Gregorian calendar)

### Key Variables for Longitudinal Analysis
From welfare atlas:
- Income (`Daramad`)
- Asset measures (cars, stocks)
- Financial activity (banking, transactions)
- Welfare program participation

To map from HEIS:
- Household expenditure by category
- Consumption patterns
- Durable goods ownership
- Housing characteristics

## Notes

**Session started:** 2025-11-12
**Data copied from:** `/Users/kevanharris/Library/CloudStorage/Dropbox/05_Data/Iran Primary Data/Welfare/2016 Welfare Atlas/`
**Project created:** This is initial setup session
