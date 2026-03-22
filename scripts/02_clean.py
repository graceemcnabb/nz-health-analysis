import pandas as pd
import sys

def clean_prevalence(filepath):
    """
    Cleans the NZ Health Survey prevalence/mean CSV file.
    Handles column renaming, publishing flags, suppressed values,
    data types, and whitespace. Returns a cleaned DataFrame.
    """

    # Load raw CSV
    df = pd.read_csv(filepath)

    # Standardise column names to snake_case
    # e.g. 'short.description' -> 'short_description'
    df.columns = (df.columns
                  .str.lower()
                  .str.replace('.', '_', regex=False)
                  .str.replace(' ', '_', regex=False))

    # Rename columns to more readable names
    df = df.rename(columns={
        'short_description': 'indicator',
        'total': 'prevalence_total',
        'total_low_ci': 'ci_low',
        'total_high_ci': 'ci_high'
    })

    # Handle publishing flags
    # Blank = publishable (fill with 'OK'), E = estimate, S = suppressed
    df['flag'] = df['flag_for_publishing'].fillna('OK')
    df['is_suppressed'] = df['flag'] == 'S'
    df['is_estimate'] = df['flag'] == 'E'

    # Set suppressed numeric values to null rather than dropping rows
    # This preserves the fact that data exists for the subgroup
    # while preventing unreliable figures from appearing in visuals
    df.loc[df['is_suppressed'], 'prevalence_total'] = None
    df.loc[df['is_suppressed'], 'male'] = None
    df.loc[df['is_suppressed'], 'female'] = None

    # Convert year to numeric — coerce handles any non-numeric values
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    # Drop rows where indicator is null — these are not usable records
    df = df.dropna(subset=['indicator'])

    # Strip leading/trailing whitespace from text columns
    # Prevents mismatches when filtering in Power BI
    text_cols = ['indicator', 'group', 'flag']
    for col in text_cols:
        df[col] = df[col].str.strip()

    # Drop original flag column now replaced by cleaner flag/is_suppressed/is_estimate columns
    df = df.drop(columns=['flag_for_publishing'])

    return df


if __name__ == '__main__':
    try:
        print("Starting...", flush=True)

        # Clean the raw prevalence file
        df = clean_prevalence('C:/Users/gemil/Data/nz-health-survey-2024-25-prevalences.csv')
        print(f"Loaded {len(df)} rows", flush=True)

        # Save cleaned output — note: raw file is never overwritten
        df.to_csv('C:/Users/gemil/Data/prevalence_clean.csv', index=False)
        print(f'Done — {len(df)} rows exported', flush=True)

    except Exception as e:
        print(f'Error: {e}', flush=True)
        sys.exit(1)