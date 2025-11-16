# Iranian Welfare Atlas 1402 (2023-24) Analysis

## Project Overview

Analysis of 2% sample welfare atlas data (1.7M individuals, ~600K households) from Iranian year 1402 (2023-24).

**Primary goal:** Understand household welfare distribution across Iran and prepare for integration with longitudinal household expenditure/consumption datasets (HEIS).

**Data source:** Iranian Welfare Database (پایگاه اطلاعات رفاهی ایرانیان) - 2% public sample
**Timeline:** Data covers years 1395-1402 (2016-2024 Gregorian) with travel data from 1395-1399 (2016-2020) and financial data from 1398-1402 (2019-2024)

## About the Iranian Welfare Database

**Official source:** Ministry of Cooperatives, Labor and Social Welfare (وزارت تعاون، کار و رفاه اجتماعی)
**Database portal:** https://refahdb.mcls.gov.ir/
**Atlas portal:** https://iran-bssc.ir/atlas/

### Database Construction

The Iranian Welfare Database is a **massive administrative data linkage project** that integrates **50 government data sources** using national ID numbers. The database contains:
- **3+ billion records** from integrated administrative systems
- **24+ million subsidy-receiving households** (nearly entire Iranian population)
- **46 sub-databases** linked at individual level
- **Registry-based data** (not survey data - reduces measurement error)

### Major Data Sources (25 integrated in Phase 1)

**Financial & Economic:**
- Central Bank of Iran (card transactions, digital payments)
- Tax Administration (registered income, business licenses)
- Tehran Stock Exchange (securities portfolios)
- Subsidy Targeting Organization (welfare transfers)

**Social Insurance:**
- Social Security Organization
- Health Insurance Organization
- State Pension Fund
- Agricultural/Rural Insurance Fund

**Welfare Programs:**
- Welfare Organization (Behzisti)
- Imam Khomeini Relief Committee (Komite Emdad)
- Martyrs Foundation

**Civil Registry:**
- Civil Registration Organization (demographics, family structure)
- Ministry of Interior (postal codes, geographic identifiers)
- Real Estate Association (property ownership)

**Education & Employment:**
- Ministry of Education (school enrollment)
- Ministry of Science (university enrollment)
- Technical and Vocational Training Organization
- Civil service employment records

**Other:**
- Law Enforcement records
- Ministry of Health
- Postal Company
- Additional 25 sources in Phase 2

### Data Linkage Methodology

1. **Primary raw database:** Data received from each source
2. **Data sources committee review:** Field-by-field validation
3. **Data cleaning:** Conflict resolution, structure unification
4. **Linkage:** All records matched using **national ID (کد ملی)**
5. **Welfare structure aggregation:** Final integrated database

### Public 2% Sample

- **Sample size:** ~1.7M individuals, ~600K households (2% of population)
- **Sampling:** Representative sample (exact methodology not documented)
- **Confidential data removed:** Some sensitive fields excluded from public release
- **Purpose:** Research and policy analysis
- **Access:** Public download at https://refahdb.mcls.gov.ir/fa/downloaddata

### Data Quality Characteristics

**Strengths:**
- Registry-based (not self-reported survey data)
- Near-universal coverage (entire population with national IDs)
- Individual-level linkage across administrative systems
- Regular updates possible from source systems

**Limitations:**
- Not all Iranians captured (informal workers without IDs, recent births)
- Some variables only for program participants (targeted welfare, travel, etc.)
- Data reflects administrative records, not ground truth (e.g., tax under-reporting)

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
- **`HasMojavezSenfi`: Business license holder (پروانه کسب)**
  - SOURCE: Iranianasnaf system - Ministry of Industry, Mining and Trade
  - WHO HAS: Shop owners, restaurant/cafe owners, artisans, service providers with physical locations
  - COVERAGE: 2.9% (individual-level, includes all household members - reasonable rate)
  - MEANING: Formal business owners registered with trade guilds (اتحادیه صنف)
  - NOTE: Does NOT include all workers - only business owners requiring trade permits
- **`ISKarmanddolat_1402`: Government employee in 1402 (2023-24)**
  - SOURCE: Civil service employment records
  - COVERAGE: 4.0% of population
  - MEANING: Active government/public sector employee
  - TAX IMPLICATION: Employer withholds taxes - individual does NOT file tax return
- `IsRetired_Asli`: Primary retirement status (94% missing - very sparse)
- `IsRetired_Tabaie`: Dependent retirement status (99.5% missing - very sparse)
- `is_bime_darman`: Health insurance coverage (19% missing)
- `IsBimePardaz`: Insurance payer (81% missing)

#### 6. Banking/Financial Data (columns 29-44)
**SOURCE:** Central Bank of Iran - comprehensive financial surveillance system
**Time-series across Iranian years 1398-1402 (2019-2024)**
**Units:** All financial variables in Rials
**COVERAGE:** 0% missing for all transaction variables - linked automatically via national ID

Bank account balances (years 1399-1400):
- `MandehAval_1399/1400`: Beginning balance (Rials) - ~19% missing (no account)
- `MandehAkhar_1399/1400`: Ending balance (Rials) - ~19% missing
- `Variz_1400`: Deposits in 1400 (Rials) - ~19% missing

Monthly transaction averages:
- **`CardPerMonth_1398/1399/1400/1401/1402`: Monthly card purchases (Rials)**
  - **CRITICAL:** 0% missing, complete coverage for all 5 years
  - **BEST CONSUMPTION PROXY** in the dataset (better than income)
  - Captures actual spending regardless of employment status
  - 76-86% of population has active card usage across all wealth deciles
- `CardBeCardPerMonth_1401/1402`: Monthly card-to-card transfers, account circulation (Rials)
- `SatnaPerMonth_1401/1402`: Monthly Satna interbank system transactions, account circulation (Rials)
- `PayaPerMonth_1401/1402`: Monthly Paya payment system transactions, account circulation (Rials)

**WHY FINANCIAL DATA IS COMPLETE:**
- Central Bank tracks ALL transactions automatically via national ID
- No individual filing or reporting required - passive administrative data
- Reflects Iran's comprehensive financial surveillance system
- Makes this dataset uniquely valuable for consumption analysis

#### 7. Assets (columns 45-47)
- `CarsPrice`: Total car value (Rials)
- `CarsCount`: Number of cars owned
- `Bourse_NetPortfoValue`: Stock exchange portfolio value (Rials)

#### 8. Income (column 48)
- **`Daramad`: Registered income in tax system (Rials)**
  - SOURCE: Tax Affairs Organization (سازمان امور مالیاتی) - my.tax.gov.ir, salary.tax.gov.ir
  - COVERAGE: Individual 26%, Household 59.3% have at least one person with registered income
  - **HOW IT WORKS:**
    - Wage earners legally EXEMPT from filing individual returns
    - ALL employers (govt + private) REQUIRED to submit salary lists electronically (Article 86, Direct Tax Law)
    - Employers submit employee names, national IDs, salaries via salary.tax.gov.ir
    - Tax Affairs Organization links submitted data to individual tax records
    - Self-employed must file individual returns for business/rental/professional income
  - **WHAT IT INCLUDES:**
    - Government employee salaries: 98.3% coverage (near-perfect employer compliance)
    - Private sector employee salaries: LOW coverage (employer non-compliance)
    - Self-employed professionals (must file returns)
    - Business owners (must file returns)
    - Property owners with rental income (must file returns)
    - Freelancers, contractors (must file returns)
  - **WHY 73% "MISSING":**
    - **Private sector employer non-compliance**: Employers required to submit salary lists, but compliance much lower than government sector
    - **Informal economy**: No registered employers to submit salary lists
    - Children (26% of population), retirees (8%), unemployed, dependents
  - **INTERPRETATION:** Daramad = employer-submitted salary data + self-filed business/rental/professional income
    - Government sector: near-perfect compliance (98.3%)
    - Private sector: low compliance (explains most of the 73% "missing")
    - Workers themselves don't file (legally exempt), but their employers are SUPPOSED to submit
    - Card spending data (0% missing) is better consumption proxy than income

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
- Geographic identifiers: 31 provinces, 466 counties, 196,390 postal codes (neighborhood-level)

### CRITICAL LIMITATION: No Ethnicity or Language Data

**This dataset contains NO individual-level ethnicity or language information.** Iran's census does not collect ethnic/linguistic data. Therefore:

- **CANNOT attribute geographic differences to ethnic identity**
- **Provinces are NOT ethnically homogeneous**:
  - Sistan-Balochistan: Baloch, Persian, and other populations
  - Kurdistan: Kurdish, Persian, Azeri populations
  - West Azerbaijan: Azeri, Kurdish, Armenian populations
  - All provinces have mixed populations
- **Geographic patterns may reflect**:
  - Urban vs rural (universal 1.3 decile gap)
  - Geographic remoteness and border regions
  - Local economic structure (formal vs informal)
  - Infrastructure and historical development
  - Security conditions
  - Possibly ethnic discrimination (but cannot be proven without individual-level data)

**Key findings from geographic analysis (see PROJECT_STATE.md 2025-11-13):**
- **Rural-urban divide is universal**: Rural areas disadvantaged across ALL provinces (not ethnic-specific)
- **Sistan-Balochistan uniquely poor**: Even rural areas (decile 3.4) worse than most other rural areas (4.1-4.6)
- **Kurdish provinces NOT disadvantaged**: Government employment 1.16x representation, similar poverty to many Persian provinces
- **Welfare programs progressive**: Baloch poor receive MORE welfare (31%) than Persian poor (21%)

**For analyses of geographic inequality:**
- Use terms like "Sistan-Balochistan province" NOT "Baloch people"
- Acknowledge multiple possible explanations beyond ethnicity
- Test urban-rural patterns, within-province heterogeneity
- Be explicit about data limitations
- For causal claims about ethnicity, would need individual-level ethnic identity data

### Understanding "Missing" Data - Not Random!

**The missingness reveals the data sources and is often INFORMATIVE, not problematic:**

#### Complete Data (0% missing) - 18 variables
- Core identifiers (id, Parent_Id, GenderId, Decile, Percentile)
- ALL financial transaction variables (1398-1402) - Central Bank linkage
- Economic status markers (govt employee, business license holder)
- **WHY:** Linked automatically via national ID, passive surveillance systems

#### Sparse by Design (50-90% missing)
- **Income (73% missing):** Only self-employed/business owners file taxes; wage employees' employers withhold
  - 26% of population + 8% children + 4% govt employees = most people legitimately don't file
  - **NOT a data quality problem** - reflects Iranian tax system structure
- **Car ownership (76% missing):** Data quality issue - actual car ownership higher than 24%
- **Travel (88% missing):** Only those who traveled have records - 88% didn't travel 2016-2020
  - Missing = didn't travel (true zero)

#### Extremely Sparse (90%+ missing) - Targeted Programs
- Welfare benefits (92-99% missing): Means-tested programs with low coverage BY DESIGN
- Retirement (94% missing): Only retirees have records
- Disability (98% missing): Only those with disabilities
- **WHY:** These are targeted/selective programs - high missingness = working as intended

#### Data Quality Issues (to be cautious about)
1. **Geographic data:** 8.3% missing province/county - data linkage failure
2. **Car ownership:** 76% missing - data quality problem, not true zeros
3. **Sample selection:** 2% sample methodology not fully documented
4. **Bank balances:** Only available 1399-1400 (2 years) vs card transactions (5 years)
5. **Digital payments:** CardBeCard/Satna/Paya only 1401-1402 (newer systems)

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

## Session Management & File Organization Policy

**CRITICAL: Prevent script/file/output bloat across sessions**

### End-of-Session Cleanup
At the end of EVERY session:
1. **Remove temporary/exploratory scripts** - Delete any test scripts, temporary analysis files, or one-off exploratory code
2. **Remove temporary output files** - Delete intermediate outputs, test figures, temporary data files
3. **Keep only essential scripts** - Retain only reusable, well-documented scripts that are part of the core analysis workflow
4. **Clean empty directories** - Remove any empty output folders created during exploration

### Session Documentation
Instead of accumulating files, document work in `PROJECT_STATE.md`:
- **Session log format**: Date, tasks completed, key findings, decisions made
- **What worked**: Successful approaches, code snippets worth remembering
- **What failed**: Approaches that didn't work (to avoid repetition)
- **File inventory**: What outputs were kept and why

### Goals
- **Prevent script bloat**: No accumulation of 10, 15, 20 scripts across sessions
- **Prevent output bloat**: Keep only final, publication-ready outputs
- **Prevent file bloat**: Remove temporary files, test outputs, intermediate results
- **Maintain clean project**: Easy to understand what exists and why

### What to Keep vs Delete
**Keep:**
- Core analysis scripts (numbered, documented, reusable)
- Final outputs (figures, tables, reports for publication)
- Derived datasets that took significant computation time
- Documentation files (CLAUDE.md, PROJECT_STATE.md)

**Delete at session end:**
- `test_*.R`, `explore_*.R`, `temp_*.R` scripts
- Temporary output files, test figures, draft tables
- Intermediate data files easily regenerated
- Empty output directories

## Open Questions

**About the data:**
- ✓ What population does the 2% sample represent? All subsidy recipients (nearly universal in Iran)
- ✓ Are sampling weights provided? No - this is administrative data snapshot, not probability sample
- ✓ Why only 14 of 31 provinces? All 31 provinces represented (initial docs incomplete)
- ✓ Units clarified: All financial variables in Rials
- ✓ Daramad = Annual registered income via employer-submitted salary lists + self-filed business/rental/professional income
- ✓ Private sector wage workers: Workers exempt from filing, BUT employers required to submit salary lists (low compliance explains 73% missing)
- How to handle missing province data (8.3% of observations)?

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
