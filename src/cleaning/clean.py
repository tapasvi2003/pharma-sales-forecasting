import pandas as pd
import numpy as np

def clean_hourly_data(df_raw):
    """
    Clean the hourly data DataFrame.
    
    Args:
        df_raw (pd.DataFrame): The DataFrame containing hourly data to be cleaned.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    
    df = df_raw.copy()

    df['datum'] = pd.to_datetime(df['datum'])

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    df['year'] = df['datum'].dt.year
    df['month'] = df['datum'].dt.month
    df['day'] = df['datum'].dt.day
    df['day_of_week'] = df['datum'].dt.dayofweek

    df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

    df['is_open'] = df['hour'].between(7,20).astype(int)

    df = df.sort_values('datum').reset_index(drop=True)

    print(f"Cleaned hourly data shape: {df.shape}")
    print(f"Date range: {df['datum'].min()} to {df['datum'].max()}")

    return df

def clean_daily_data(df_raw):

    """
    clean the daily data DataFrame.

    Args:
        df_raw (pd.DataFrame): The DataFrame containing daily data to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame.

    """

    df = df_raw.copy()

    df['datum'] = pd.to_datetime(df['datum'])

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    df = df.drop(columns=['year', 'month', 'hour', 'weekday_name'])

    df['year'] = df['datum'].dt.year
    df['month'] = df['datum'].dt.month  
    df['day'] = df['datum'].dt.day
    df['day_of_week'] = df['datum'].dt.dayofweek

    df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

    df = df.sort_values('datum').reset_index(drop=True)

    print(f"Cleaned daily data shape: {df.shape}")
    print(f"Date range: {df['datum'].min()} to {df['datum'].max()}")

    return df

def clean_weekly_data(df_raw):
    """
    clean the weekly data DataFrame.

    Args:
        df_raw (pd.DataFrame): The DataFrame containing weekly data to be cleaned.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """

    df = df_raw.copy()

    df['datum'] = pd.to_datetime(df['datum'])

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    df['year'] = df['datum'].dt.year
    df['month'] = df['datum'].dt.month
    df['week_number'] = df['datum'].dt.isocalendar().week

    df = df.sort_values('datum').reset_index(drop = True)

    print(f"Cleaned weekly data shape: {df.shape}")
    print(f"Date range: {df['datum'].min()} to {df['datum'].max()}")

    return df

def clean_monthly_data(df_raw):
    """
    clean the monthly data DataFrame.

    Args:
        df_raw (pd.DataFrame): The DataFrame containing monthly data to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    
    """
    df = df_raw.copy()

    df['datum'] = pd.to_datetime(df['datum'])

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    df['year'] = df['datum'].dt.year
    df['month'] = df['datum'].dt.month

    df = df.sort_values('datum').reset_index(drop = True)

    print(f"cleaned monthly data shape: {df.shape}")
    print(f"Date range: {df['datum'].min()} to {df['datum'].max()}")

    return df

