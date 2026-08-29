import pandas as pd
import numpy as np
import os
import sys

#Adding the parent directory to the system path to allow imports from the 'src' directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

def extract(filename):
    """
    Extract a single CSV file from RAW data path
    Args:
        filename (str): The name of the file to be extracted (e.g., 'data.csv')

    Returns:
        pd.DataFrame: Load DataFrame
    """
    
    filepath = os.path.join(RAW_DATA_PATH, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)

    print(f"Extracted {filename}: {df.shape}")
    return df

def transform(df, granularity):
    """
    Transform the raw DataFrame using the cleaning functions based on the specified granularity.

    Args:
        df : raw dataframe
        granularity: 'hourly', 'daily', 'weekly', or 'monthly'
    
    Returns:
        pd.DateFrame: cleaned DataFrame
    
    """

    from cleaning.clean import clean_hourly_data, clean_daily_data, clean_weekly_data, clean_monthly_data

    if granularity == 'hourly':
        return clean_hourly_data(df)
    elif granularity == 'daily':
        return clean_daily_data(df)
    elif granularity == 'weekly':
        return clean_weekly_data(df)
    elif granularity == 'monthly':
        return clean_monthly_data(df)
    else:
        raise ValueError(f"Invalid granularity: {granularity}. Must be one of 'hourly', 'daily', 'weekly', or 'monthly'.")
    
def load(df, filename):
    """
    Save cleaned dataframe to PROCESSED data path as a CSV file.

    Args:
        df (pd.DataFrame): The cleaned DataFrame to be saved.
        filename (str): The name of the file to save the cleaned DataFrame (e.g., 'cleaned_data.csv').
    
    Returns:
        None
    """
    df.to_csv(os.path.join(PROCESSED_DATA_PATH, filename), index=False)
    print(f"Saved cleaned data to {filename} at {PROCESSED_DATA_PATH+filename}")


def run_pipeline():
    """ 
    RUN the ETL pipeline for all datasets (hourly, daily, weekly, monthly).

    """
    files = {
        'hourly': 'saleshourly.csv',
        'daily': 'salesdaily.csv',
        'weekly': 'salesweekly.csv',
        'monthly': 'salesmonthly.csv'
    }

    for granularity, filename in files.items():
        print(f"Processing {granularity} data...")
        df_raw = extract(filename)
        df_cleaned = transform(df_raw, granularity)
        load(df_cleaned, f"cleaned_{granularity}.csv")

if __name__ == "__main__":
    run_pipeline()

