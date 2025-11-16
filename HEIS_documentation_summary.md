# HEIS Documentation Summary

## Available Documentation Files

### Primary Documentation
1. **Variable Metadata** (English/Farsi):
   - `Iran_Household_Budget_Survey_Summary_1402.xlsx` (25MB)
   - Contains 130 variable definitions with English names, Farsi names, and descriptions
   - Covers aggregated household-level variables

2. **Variable Availability Over Time**:
   - `Household_Expenditure_Income_Survey_Variables_1363-1398.xlsx`
   - Documents which variables/sections available in each year 1363-1398
   - Tracks changes in occupational coding, insurance questions, income sections

3. **Questionnaires** (34 PDFs):
   - Location: `questionnaires/` folder
   - Coverage: Years 1363-1392 (1984-2013)
   - Both annual PDFs and separate urban/rural questionnaires
   - Most recent: Household_Survey_Questionnaire_92.pdf (year 1392 / 2013)

### Secondary Documentation
4. **Year-Specific Documentation** (scattered across folders):
   - Year 1373: 2 files (HTML + DOC)
   - Year 1380-1382: Documentation and survey forms
   - Year 1384: Structure documentation
   - Format: .doc, .htm, .rtf files

5. **Student Documentation** (Zep Kalb):
   - `2021 HEIS insurance overview (Kalb).docx` - Insurance variable analysis
   - `2021 HEIS Mega-codebook explanation (Kalb).xlsx` - Variable availability matrix
   - Key finding: Insurance questions stable since mid-1990s, but 2007-8 rupture in SSO payment system

## HEIS Data Structure

### Raw Data Variables (P1 - Household Roster)
The raw HEIS P1 data uses **DYCOL codes** (dynamic columns) that are NOT directly interpretable without codebook:

| Variable | Likely Meaning | Based on Metadata |
|----------|---------------|-------------------|
| Address | 11-digit household ID | Encodes province/county/enumeration area |
| DYCOL01 | Relation to head | 18 categories (1=head, 2=spouse, 3=child, etc.) |
| DYCOL03 | Unknown - NOT binary sex | 9 categories (need questionnaire to decode) |
| DYCOL04 | Unknown - NOT age | Values 1-2 (categorical, not years) |
| DYCOL05 | Likely AGE | Values 0-99 (age in years) |
| DYCOL06 | Education or other | High missingness (6.3%) |
| DYCOL07 | Literacy or other | Multiple categories |
| DYCOL08 | Occupation code | ISCO codes (3-digit pre-1379, 4-digit ISCO-88 from 1379) |
| DYCOL09 | Employment/Activity status | 6 categories |
| DYCOL10 | Insurance coverage | 4 categories |

**CRITICAL**: Variable numbering/ordering may differ from expected patterns. Need actual questionnaire PDFs to confirm.

### Aggregated Data Variables (Summary File)
The summary file contains clean, labeled variables at household level:

**Demographics:**
- Family Size, Number of Spouses, Number of Children
- Head: Sex, Age, Literacy, Education Level, Marital Status, Activity Status
- Spouse: Same characteristics as head

**Housing:**
- Tenure, Structure Type, House Area, Number of Rooms
- Utilities: Water, Electricity, Gas, Sewerage
- Appliances: 20+ variables (TV, PC, Internet, Car, etc.)

**Expenditures:**
- Net Expenditure, Gross Expenditure
- 22 expenditure categories (COICOP classification)
- Food: 11 subcategories
- Housing, Health, Transport, Education, etc.

**Income:**
- Total Income, Active Income, Passive Income
- Employment Income: Cash/NonCash × Private/Public/Cooperative
- Self-Employed: Agricultural/NonAgricultural/Home Production
- Passive: Rent (actual + imputed), Aid/Transfer, Subsidies, Interest, Retirement

## Key Findings from Student Documentation

### Variable Consistency Issues (Kalb)
1. **Insurance questions**: Relatively stable since mid-1990s
2. **2007-8 rupture**: SSO payment system change (not survey format change)
3. **Occupational coding changes**:
   - 1369: Occupational system introduced
   - 1376: 3-digit codes
   - 1379: 4-digit ISCO-88
   - 1395: Major change (moved to later questionnaire section?)

### Coverage Patterns
- **Health insurance**: Rose from 23% (2000) to 89% (2017)
- **Pension insurance**: Stable 30-33% (2006-2017)
- **Class disparities**: Bottom quintile 84% health coverage vs top quintile 59% pension coverage (2017)

## Geographic Coding

### Address Structure (11 digits)
First 2 digits appear to be province code (e.g., "20" appears frequently in sample).
Full structure likely: Province (2) + County (2) + District/EA (7)

Need official Statistical Center of Iran geographic codes to decode.

## Panel Structure

HEIS is a **rotating panel**:
- 16% of households (18,114) appear in 2 consecutive years (1397-1398)
- 84% appear only once (cross-sectional)
- NOT a true longitudinal panel - households rotate in/out

## Recommendations

### For Variable Decoding
1. **Obtain questionnaire PDFs for 1395-1398** (or closest years: 1392 available)
2. **Use vision analysis** on questionnaire PDFs to extract:
   - P1 roster variable definitions
   - P2 housing variable codes
   - P3 expenditure item codes
   - P4 income source codes

3. **Cross-reference with metadata** from summary file for validation

### For Analysis
1. **Use weights** (`weight` variable in Data tables) - essential for population estimates
2. **Account for rotating panel** - households not tracked longitudinally
3. **Be aware of variable changes** - especially occupational codes (1395 had major change)
4. **Geographic analysis**: Need to decode Address or obtain province/county variables from Statistical Center

### For Integration with Welfare Atlas
1. **Year 1398 overlap** - both datasets have 2019-20 data
2. **Compare definitions**:
   - HEIS income vs Welfare Atlas Daramad (registered income)
   - HEIS expenditure vs Welfare Atlas CardPerMonth (card spending)
3. **Geographic matching**: Welfare Atlas has province names, HEIS has codes - need crosswalk

## Next Steps

1. Extract P1 variable definitions from questionnaire PDF (1392 or closest)
2. Decode Address structure to extract province/county
3. Create proper variable labels for DYCOL fields
4. Build comparison framework between HEIS and Welfare Atlas
5. Consider requesting additional documentation from Statistical Center of Iran
