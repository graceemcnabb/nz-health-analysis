import pandas as pd
import sys

def clean_time_series(filepath):
    """
    Cleans the NZ Health Survey changes-over-time CSV file.
    The raw file is in wide format with one column per survey year.
    This function reshapes it to long format (one row per indicator/group/year)
    and joins prevalence values with their corresponding p-values.
    Returns a cleaned long-format DataFrame.
    """

    # Load raw CSV
    df = pd.read_csv(filepath)

    # Standardise column names to snake_case
    # e.g. 'short.description' -> 'short_description'
    df.columns = (df.columns
                  .str.lower()
                  .str.replace('.', '_', regex=False)
                  .str.replace(' ', '_', regex=False))

    # Rename the unnamed index column (row numbers 1,2,3...) to id
    # This column has no header in the raw file
    df = df.rename(columns={'unnamed:_0': 'id'})

    # Rename indicator column for consistency with other cleaned files
    df = df.rename(columns={'short_description': 'indicator'})

    # Strip whitespace and standardise indicator names to title case
    df['indicator'] = df['indicator'].str.strip().str.title()
    df['group'] = df['group'].str.strip()

    # Identify the two sets of year columns to reshape separately
    # percent_11 through percent_24 = prevalence values per year
    # p_value_24_11 through p_value_24_23 = p-values comparing each year to 2024
    percent_cols = [c for c in df.columns if c.startswith('percent_')]
    pvalue_cols = [c for c in df.columns if c.startswith('p_value_24_')]
    id_cols = ['id', 'population', 'group', 'indicator']

    # Reshape prevalence columns from wide to long format
    # Before: one row per indicator/group with 13 year columns
    # After: one row per indicator/group/year with a single prevalence column
    df_percent = df[id_cols + percent_cols].melt(
        id_vars=id_cols,
        value_vars=percent_cols,
        var_name='year_raw',
        value_name='prevalence'
    )

    # Extract numeric year from column name
    # e.g. 'percent_11' -> 11 -> 2011
    df_percent['year'] = df_percent['year_raw'].str.replace('percent_', '').astype(int) + 2000
    df_percent = df_percent.drop(columns=['year_raw'])

    # Reshape p-value columns from wide to long format using same approach
    df_pvalue = df[id_cols + pvalue_cols].melt(
        id_vars=id_cols,
        value_vars=pvalue_cols,
        var_name='pval_raw',
        value_name='p_value'
    )

    # Extract numeric year from p-value column name
    # e.g. 'p_value_24_11' -> 11 -> 2011
    df_pvalue['year'] = df_pvalue['pval_raw'].str.extract(r'p_value_24_(\d+)').astype(int) + 2000
    df_pvalue = df_pvalue.drop(columns=['pval_raw'])

    # Join prevalence and p-value DataFrames on id and year
    # Left join preserves all prevalence rows even where no p-value exists
    df_long = df_percent.merge(
        df_pvalue[['id', 'year', 'p_value']],
        on=['id', 'year'],
        how='left'
    )

    # Flag indicators with a statistically significant change vs 2024
    # Standard significance threshold of p < 0.05
    df_long['significant_change'] = df_long['p_value'] < 0.05

    # Add decade grouping for high-level trend analysis in Power BI
    df_long['decade'] = (df_long['year'] // 10 * 10).astype(str) + 's'

    # Drop rows where prevalence is null — no usable value for that year/group
    df_long = df_long.dropna(subset=['prevalence'])

    # Strip embedded flag characters from prevalence values
    # The raw file stores flags inline e.g. '9.4 e' or '12.3 s'
    # Extract only the numeric portion to allow Power BI to read as decimal
    df_long['prevalence'] = df_long['prevalence'].astype(str).str.extract(r'([\d.]+)').astype(float)

    return df_long


def clean_rate_ratios(filepath):
    """
    Cleans the NZ Health Survey subgroup comparisons CSV file.
    Contains adjusted rate ratios comparing population groups for 2024/25.
    A rate ratio > 1 indicates the comparison group faces elevated risk
    relative to the reference group.
    Returns a cleaned DataFrame.
    """

    # Load raw CSV
    df = pd.read_csv(filepath)

    # Standardise column names to snake_case
    df.columns = (df.columns
                  .str.lower()
                  .str.replace('.', '_', regex=False)
                  .str.replace(' ', '_', regex=False))

    # Rename columns for clarity and consistency with other cleaned files
    df = df.rename(columns={
        'short_description': 'indicator',
        'adjusted_rate_ratio': 'rate_ratio',
        'adjusted_rate_ratio_low_ci': 'rate_ratio_ci_low',
        'adjusted_rate_ratio_high_ci': 'rate_ratio_ci_high',
        'adjusted_for': 'adjusted_for'
    })

    # Strip whitespace and standardise indicator names to title case
    df['indicator'] = df['indicator'].str.strip().str.title()
    df['comparison'] = df['comparison'].str.strip()

    # Calculate confidence interval width as a data quality indicator
    # A wider CI indicates more uncertainty around the rate ratio estimate
    # Renamed to margin_of_error for stakeholder readability
    df['margin_of_error'] = df['rate_ratio_ci_high'] - df['rate_ratio_ci_low']

    # Boolean flag for indicators where the comparison group faces elevated risk
    # rate_ratio > 1 means the comparison group has higher prevalence than reference
    df['elevated_risk'] = df['rate_ratio'] > 1

    # Convert year to numeric — this file covers 2024/25 only
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    # Drop rows where indicator is null — not usable records
    df = df.dropna(subset=['indicator'])

    return df


if __name__ == '__main__':
    try:
        # Clean the time series file
        print("Cleaning time series...", flush=True)
        df_time = clean_time_series('C:/Users/gemil/Data/nz-health-survey-2024-25-time-series.csv')
        df_time.to_csv('C:/Users/gemil/Data/time_series_clean.csv', index=False)
        print(f"Done — {len(df_time)} rows, {len(df_time.columns)} columns", flush=True)
        print(f"Columns: {df_time.columns.tolist()}", flush=True)

        # Clean the rate ratios file
        print("\nCleaning rate ratios...", flush=True)
        df_ratios = clean_rate_ratios('C:/Users/gemil/Data/nz-health-survey-2024-25-rate-ratios.csv')
        df_ratios.to_csv('C:/Users/gemil/Data/rate_ratios_clean.csv', index=False)
        print(f"Done — {len(df_ratios)} rows, {len(df_ratios.columns)} columns", flush=True)
        print(f"Columns: {df_ratios.columns.tolist()}", flush=True)

    except Exception as e:
        print(f'Error: {e}', flush=True)
        sys.exit(1)
