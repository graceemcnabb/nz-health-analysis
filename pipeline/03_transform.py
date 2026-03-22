import pandas as pd
import sys

def transform(df):
    """
    Applies feature engineering to the cleaned prevalence DataFrame.
    Creates derived columns to support Power BI analysis and improve
    slicer usability. Returns the transformed DataFrame.
    """

    # Confidence interval width — measures estimate precision
    # A wider CI indicates more uncertainty around the prevalence figure
    df['ci_width'] = df['ci_high'] - df['ci_low']

    # Absolute difference between male and female prevalence
    # Used to identify indicators with the largest gender disparities
    df['gender_gap'] = abs(df['male'] - df['female'])

    # Categorise the 71 unique group values into 6 meaningful categories
    # This makes Power BI slicers far more usable than raw group strings
    def categorise_group(group):
        if pd.isna(group):
            return 'Unknown'
        group_lower = group.lower()
        if any(x in group_lower for x in ['māori', 'maori', 'pacific', 'asian', 'european']):
            return 'Ethnicity'
        if any(x in group_lower for x in ['15-24', '25-34', '35-44', '45-54', '55-64', '65+']):
            return 'Age Group'
        if any(x in group_lower for x in ['quintile']):
            return 'Deprivation'
        if any(x in group_lower for x in ['male', 'female']):
            return 'Gender'
        if 'region' in group_lower:
            return 'Health Region'
        if 'total' in group_lower:
            return 'Total Population'
        return 'Other'

    # Apply categorisation to every row in the group column
    df['group_category'] = df['group'].apply(categorise_group)

    # Group years into decades (e.g. 2011 -> '2010s') for high-level trend grouping
    df['decade'] = (df['year'] // 10 * 10).astype(str) + 's'

    # Boolean flag indicating whether prevalence is above the dataset median
    # Useful for quickly filtering high-burden indicators in Power BI
    df['high_prevalence'] = df['prevalence_total'] > df['prevalence_total'].median()

    # Standardise indicator names to title case for consistent Power BI labels
    # e.g. 'current smokers' -> 'Current Smokers'
    df['indicator'] = df['indicator'].str.title()

    # Handle male and female publishing flags separately
    # Same logic as the total flag in 02_clean.py — suppressed values set to null
    df['male_flag'] = df['male_flag_for_publishing'].fillna('OK').str.strip()
    df['female_flag'] = df['female_flag_for_publishing'].fillna('OK').str.strip()
    df['male_is_suppressed'] = df['male_flag'] == 'S'
    df['female_is_suppressed'] = df['female_flag'] == 'S'

    # Null out suppressed male/female values to prevent unreliable figures in visuals
    df.loc[df['male_is_suppressed'], 'male'] = None
    df.loc[df['female_is_suppressed'], 'female'] = None

    # Drop original flag columns now replaced by cleaner boolean columns
    df = df.drop(columns=['male_flag_for_publishing', 'female_flag_for_publishing'])

    return df


if __name__ == '__main__':
    try:
        print("Starting...", flush=True)

        # Load cleaned output from 02_clean.py
        df = pd.read_csv('C:/Users/gemil/Data/prevalence_clean.csv')
        print(f"Loaded {len(df)} rows", flush=True)

        # Apply feature engineering transformations
        df = transform(df)

        # Save final analysis-ready file for Power BI
        df.to_csv('C:/Users/gemil/Data/prevalence_final.csv', index=False)
        print(f"Done — {len(df)} rows, {len(df.columns)} columns exported", flush=True)
        print(f"Columns: {df.columns.tolist()}", flush=True)

    except Exception as e:
        print(f'Error: {e}', flush=True)
        sys.exit(1)
