import pandas as pd

# =============================================================================
# 05_validate.py
# Validation and exploration script used throughout dashboard development.
# Run individual sections as needed to verify data integrity, check filter
# outputs, and confirm values match what Power BI visuals are displaying.
# Sections can be commented/uncommented as needed.
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1: Health Risk Indicator Discovery
# Searches the prevalence file for indicators matching known health risk keywords.
# Used to identify which indicators to feature in the dashboard.
# -----------------------------------------------------------------------------

df = pd.read_csv('C:/Users/gemil/Data/prevalence_final.csv')

# Keywords covering major NZ health risk areas
risk_keywords = [
    'obes', 'smok', 'diabet', 'depres', 'anxiet', 'mental',
    'alcohol', 'hazardous', 'overweight', 'physical inactiv',
    'cannabis', 'hypertens', 'asthma', 'cardiovascular',
    'cancer', 'stroke', 'heart', 'suicide', 'self-harm',
    'adhd', 'autism', 'disability', 'vaping', 'e-cigarette'
]

# Filter to rows where indicator name matches any keyword
mask = df['indicator'].str.lower().str.contains('|'.join(risk_keywords), na=False)
risk_df = df[mask]

# Show top 25 risk indicators by maximum prevalence across all subgroups
summary = (risk_df.groupby('indicator')['prevalence_total']
           .max()
           .sort_values(ascending=False)
           .head(25))

# Uncomment to run
# print(summary.to_string())


# -----------------------------------------------------------------------------
# SECTION 2: Single Indicator Verification
# Checks the exact value for a specific indicator, year, and group combination.
# Used to verify DAX measure outputs match the underlying data.
# e.g. confirms Obesity Rate KPI card should show 34.2% for adults/Total/2024
# -----------------------------------------------------------------------------

df = pd.read_csv('C:/Users/gemil/Data/prevalence_final.csv')

result = df[
    (df['indicator'] == 'Obese') &
    (df['year'] == 2024) &
    (df['group'] == 'Total')
][['indicator', 'population', 'group', 'year', 'prevalence_total']]

# Uncomment to run
# print(result.to_string())


# -----------------------------------------------------------------------------
# SECTION 3: Time Series Group & Population Check
# Verifies the unique group and population values in the time series file.
# Used to confirm filter values before applying them to Power BI visuals.
# Also checks a specific indicator to verify the wide-to-long reshape worked
# correctly and prevalence values are numeric (not text with embedded flags).
# -----------------------------------------------------------------------------

df = pd.read_csv('C:/Users/gemil/Data/time_series_clean.csv')

# Uncomment individual lines as needed
# print(df['group'].unique())
# print(df['population'].unique())
# print(df[df['indicator'] == 'Obese'][['indicator', 'group', 'population', 'year', 'prevalence']].head(20))


# -----------------------------------------------------------------------------
# SECTION 4: Full Indicator List for Dashboard Filtering
# Prints all unique adult/total population indicators from the time series file.
# Used to decide which indicators to include or exclude from Power BI visuals.
# -----------------------------------------------------------------------------

pd.set_option('display.max_rows', None)

df = pd.read_csv('C:/Users/gemil/Data/time_series_clean.csv')

# Filter to total population adults only to get the clean indicator list
total = df[
    (df['group'] == 'Total') &
    (df['population'] == 'adults')
]

# Print all indicators alphabetically
indicators = sorted(total['indicator'].unique())
for i in indicators:
    print(i)