# Iranian Welfare Atlas 1402 - What We Know

## Dataset Overview

**Official name:** Iranian Welfare Database (پایگاه اطلاعات رفاهی ایرانیان)
**Owner:** Ministry of Cooperatives, Labor and Social Welfare
**Portal:** https://refahdb.mcls.gov.ir/
**Scale:** Links 50 administrative data sources using national IDs (3+ billion records, 24+ million households)
**Public sample:** 2% sample (~1.7M individuals, 596K households) with confidential fields removed
**Coverage:** Subsidy recipients (nearly universal in Iran - not a probability sample)

**Data structure:**
- 1,697,816 individuals
- 595,688 households (via Parent_Id linkage)
- 48 variables
- Time coverage: Years 1395-1402 (2016-2024), with varying coverage by variable type

**Major linked data sources:**
- Central Bank of Iran: ALL card transactions 2019-2024 (0% missing)
- Tax Affairs Organization: Registered income, business licenses
- Social Security Organization, Health Insurance
- Welfare programs (Behzisti, Komite Emdad)
- Civil Registration: Demographics, addresses
- Tehran Stock Exchange: Securities portfolios

## Key Variable Definitions

### Daramad (Registered Income)
**What it is:** Income registered in the Tax Affairs Organization database
**Coverage:** Individual 26%, Household 59.3%

**How it works:**
- Wage earners legally EXEMPT from filing individual returns
- ALL employers required to submit salary lists electronically (Article 86, Direct Tax Law)
- System: salary.tax.gov.ir - employers submit employee names, national IDs, salaries
- Data automatically linked to individual tax records

**What it captures:**
- Government employee salaries: 98.3% coverage (near-perfect employer compliance)
- Private sector employee salaries: LOW coverage (~11% in some provinces)
- Self-employed, business owners, landlords, professionals (must file individual returns)

**Why 73% missing:**
- Private sector employers: low compliance with salary list submission requirement
- Informal economy: no registered employers
- Children (26%), retirees (8%), unemployed, dependents

**Interpretation:** Daramad = employer-submitted salary data + self-filed business/rental income
**NOT individual wage earner filings**

### ISKarmanddolat_1402 (Government Employee)
- Individual: 4.0% of working-age
- Household: 10.2% have at least one government employee
- Source: Civil service employment records
- 98.3% have Daramad (salaries administratively reported)

### HasMojavezSenfi (Business License)
- Individual: 2.9% of working-age
- Household: 8.0% have at least one license holder
- Source: Iranianasnaf system (Ministry of Industry, Mining, Trade)
- Who: Shop owners, restaurant/cafe owners, artisans, service providers
- Only 10% of Daramad holders have business license (most Daramad from professionals, landlords, govt employees)

### IsBimePardaz (Insurance Payer / Formal Employment)
- Individual: 18.7% of working-age
- Source: Social Security Organization + government employee insurance
- Breakdown: 79% SSO (private sector), 21% government

### CardPerMonth_1398-1402 (Card Spending)
**BEST CONSUMPTION PROXY in dataset**
- 0% missing (complete coverage via Central Bank linkage)
- 76-86% active card usage across all wealth deciles
- Monthly card purchases in Rials
- Superior to income data for consumption analysis

### Decile & Percentile (Wealth Measures)
**NOT consumption-based poverty** - these are asset/wealth measures
Based on (from Ilam PDF methodology):
- Assets, salary, insurance, foreign travel, car/home ownership
- Bank deposits 2016-2019
- Card transactions 2019-2020

**For poverty analysis:** Use card spending or HEIS consumption data, not wealth deciles

### Asset Variables (Cars, Stocks)
**Missing = zero ownership** (storage optimization)
- CarsCount/CarsPrice: 76% missing = no car (not unknown)
- Bourse_NetPortfoValue: missing = no stock portfolio
- Stocks explicitly code zero (dense encoding, not missing=zero)
- Household-level: 57% own cars, 43% don't

### Travel Variables (1395-1399 / 2016-2020)
**Definition:** International non-pilgrimage air travel ONLY
- 12% traveled, 88% didn't (true zeros, not missing data)
- Matches official statistics (2019: 7-10M of 82M = 8-12% traveled abroad)

### Welfare Programs
**Genuinely low coverage by design** (targeted poverty programs, not universal):
- Komite Emdad: 5.2% national coverage (ground truth: 5-6%)
- Behzisti: 2.2% national coverage (ground truth: 3.6%)
- Nutrition subsidy: 0.2%

**Targeting effectiveness:**
- Komite: 27.6% coverage in poorest decile → 0.1% in richest (226:1 ratio)
- Among bottom 3 deciles: Baloch poor 31%, Kurdish poor 24%, Persian poor 21%
- Programs are progressive and well-targeted

## Geographic Patterns

### CRITICAL METHODOLOGICAL LIMITATION
**This dataset contains NO individual-level ethnicity or language data.**
Iran's census does not collect ethnic/linguistic information.

**Implications:**
- CANNOT attribute provincial differences to ethnic identity
- Provinces are NOT ethnically homogeneous (mixed populations)
- Geographic patterns may reflect: remoteness, local economy, urban/rural, infrastructure, security, historical development
- For causal claims about ethnicity, would need individual-level ethnic identity data

**Data granularity available:**
- 31 provinces
- 466 counties (شهرستان)
- 196,390 unique 7-digit postal codes (neighborhood-level)
- Urban/rural indicator

### Urban-Rural Divide (Universal Pattern)
**Rural Iran:** Decile 4.6, 42% bottom 3, 2.4% govt employment, 19% Daramad
**Urban Iran:** Decile 5.9, 24% bottom 3, 4.7% govt employment, 30% Daramad
**Gap:** 1.3 deciles

This pattern holds in ALL provinces - not ethnic-specific.

### Provincial Patterns

**Sistan-Balochistan (poorest province):**
- Overall: Decile 3.9, 56% bottom 3
- Urban: Decile 4.4, 49% bottom 3
- Rural: Decile 3.4, 64% bottom 3 (worse than most other rural areas: 4.1-4.6)
- Only 52% urban (vs 86% national)
- Government employment: 0.83x population share (under-represented)
- Employer compliance: 10.8% Daramad (vs 21-29% in similarly poor provinces)
- Welfare targeting: 31% of poor receive programs (HIGHER than Persian 21%)
- County deciles range 2.7 to 4.8 (significant within-province heterogeneity)

**Kurdish provinces (Kurdistan, Kermanshah, Ilam):**
- Decile 5.0-5.3 (similar to many Persian-majority provinces)
- Government employment: 1.16x (OVER-represented)
- Urban Kurdistan: Decile 5.5, comparable to other urban areas
- Rural Kurdistan: Decile 4.2, similar to other rural areas
- Pattern: Regional poverty, not ethnic-specific disadvantage

**Azeri provinces:**
- Decile 5.2-5.3, comparable to Persian provinces
- Government employment: 0.87x (slightly under-represented)

**Khuzestan/Arab:**
- Decile 5.1
- Government employment: 1.02x (perfectly proportional)

**Government employment representation:**
- Kurdish: 1.16x, Arab: 1.02x, Azeri: 0.87x, Baloch: 0.83x
- Pattern: NOT uniform ethnic discrimination

**Possible explanations for Sistan-Balochistan disadvantage:**
1. Geographic remoteness (border region)
2. Security/border insecurity
3. High rurality (52% vs 86% national)
4. Limited formal economy / informal employment
5. Historical underinvestment in infrastructure
6. Employer non-compliance with tax reporting
7. Possibly ethnic discrimination (cannot be proven without individual-level data)

## Data Quality

### Complete Data (0% missing)
- Core identifiers: id, Parent_Id, GenderId
- Wealth: Decile, Percentile
- Employment: HasMojavezSenfi, ISKarmanddolat_1402
- Financial transactions (ALL years 1398-1402): CardPerMonth, CardBeCard, Satna, Paya

### Moderate Missing (8-30%)
- Geographic: 8.3% missing province/county
- Urban/rural: 2.4% missing
- Daramad: 73% (explained by tax system - not data quality issue)

### Asset Variables
- Missing = zero ownership (storage optimization)
- 57% households own cars, 43% don't
- Stocks explicitly code zeros (dense encoding)

### High Missing (>90%) - By Design
- Welfare programs: Targeted, not universal (5-6% coverage is correct)
- Retirement: 5.8% (only retirees)
- Disability: 98%+ (only those with disabilities)
- Travel: 88% (true zeros - didn't travel 2016-2020)

### Known Data Quality Issues
- Geographic: 8.3% missing province/county (data linkage failure)

## Key Findings

### Employment & Income
- 38.5% of households have NO formal employment indicators (govt job, business license, or registered income)
- Government employees: Near-perfect tax system integration (98.3% have Daramad)
- Private sector: Low employer tax compliance varies by province (11-30% Daramad coverage)
- Informal economy substantial, especially in rural areas and border regions

### Wealth & Consumption
- Wealth deciles measure ASSETS, not consumption
- Card spending (0% missing) is best consumption proxy available
- For proper poverty measurement: Need HEIS consumption data

### Gender Patterns
- Female labor force participation: 16.9% (matches official statistics)
- Female-headed households: 22.3% (widowhood, not sampling bias)
  - Average age 53 vs male heads 48
  - 58% single-person households
  - Concentrated in poverty (52% poorest decile)

### Health Insurance
- 81.3% have coverage (primary + dependents)
- 18.7% are payers (primary insured, employed)
- Young men 18-25 experience coverage gaps (military service, informal employment)

### Welfare Programs
- Komite Emdad: 5.2% coverage, exceptional targeting (226:1 poor-to-rich ratio)
- Behzisti: 2.2% coverage
- Only 7.5% receive ANY poverty program (narrow but well-targeted)
- Baloch poor MORE likely to receive welfare than Persian poor

## Files Created

### Data
- `data/welfare_atlas_1402.parquet` - Primary working file (80MB vs 338MB CSV)
- `data/codebook.csv` - Variable definitions (Persian)
- `output/01_data_preparation/household_data.rds` - Household-level dataset (595K households)

### Documentation
- `docs/validation_2025-11-13.txt` - Ground truth validation findings
- `docs/split_pages/[province]/` - Split PDF pages for Ilam, Tehran, Kurdistan, Bushehr

### Scripts
- `scripts/00_convert_to_parquet.R` - CSV→Parquet conversion

## Open Questions

**Data interpretation:**
- How to handle 8.3% missing province data?
- Best approach for combining with HEIS consumption data?

**Life course dynamics (requires qualitative research):**
- What do uninsured young men (20-25) do during coverage gaps?
- How long does post-military job search typically last?
- Do families maintain voluntary coverage for adult children?

## Technical Notes

**Data format:** Parquet (76% compression, faster access)
**Computation:** `data.table` for efficiency (1.7M rows)
**Encoding:** UTF-8 (Persian text working correctly)
**Household linkage:** Parent_Id enables both individual and household analysis
