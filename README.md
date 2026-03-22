# NZ Health Survey Analysis — End-to-End Data Pipeline & Power BI Dashboard

An end-to-end data analytics project analysing 14 years of New Zealand population 
health data from the Ministry of Health NZ Health Survey (2011–2025). The project 
demonstrates a complete analyst workflow: raw data ingestion, Python cleaning pipeline, 
Power BI data modelling, and a four-page interactive dashboard.

---

## Key Findings

- The most deprived vs least deprived women show a daily smoking rate ratio of **6.33** 
  — the starkest equity gap in the dataset
- **Quintile 5 (most deprived)** consistently shows the highest prevalence across all 
  risk indicators including obesity, smoking, and hazardous drinking
- **Pacific populations** show the highest obesity prevalence by ethnicity; 
  **Māori** show the highest daily smoking rates — consistent with longstanding 
  health equity research in NZ

---

## Dashboard Preview

![Executive Summary](screenshots/executive-summary.png)
![Trends Over Time](screenshots/trends-over-time.png)
![Health Equity](screenshots/health-equity.png)
![Population Deep Dive](screenshots/population-deep-dive.png)

---

## Dashboard Pages

| Page | Title | Description |
|---|---|---|
| 1 | Executive Summary | KPI cards, top indicators by prevalence, gender comparison table |
| 2 | NZ Health Trends Over Time | Line chart, biggest movers bar chart, significant change table |
| 3 | NZ Health Equity Analysis | Rate ratios by group, elevated risk count, deprivation analysis |
| 4 | Population Deep Dive | Age group, ethnicity, deprivation, and gender breakdowns |

---

## Data Sources

Three CSV files downloaded from the 
[NZ Health Survey Annual Data Explorer](https://minhealthnz.shinyapps.io/nz-health-survey-2024-25-annual-data-explorer/):

| File | Rows (cleaned) | Description |
|---|---|---|
| Prevalence/Mean | 47,708 | Prevalences for total population and subgroups |
| Changes Over Time | 82,595 | Longitudinal data reshaped from wide to long format |
| Subgroup Comparisons | 3,198 | Adjusted rate ratios for 2024/25 |

**Total: ~133,500 rows across 180+ health indicators spanning 2011–2025**

---

## Python Pipeline

Five scripts process the raw data into analysis-ready CSVs:
