import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add backend directory to path so we can import data_engine
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from data_engine import fetch_fuelhh, fetch_windfor

def fetch_january_data():
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 1, 31)
    
    actual_dfs = []
    forecast_dfs = []
    
    current_date = start_date
    print("Fetching data for January 2025...")
    while current_date <= end_date:
        d_str = current_date.strftime("%Y-%m-%d")
        print(f"Fetching {d_str}...")
        
        try:
            actual = fetch_fuelhh(d_str)
            if not actual.empty:
                actual_dfs.append(actual)
        except Exception as e:
            print(f"Error fetching actuals for {d_str}: {e}")
            
        try:
            forecast = fetch_windfor(d_str)
            if not forecast.empty:
                forecast_dfs.append(forecast)
        except Exception as e:
            print(f"Error fetching forecasts for {d_str}: {e}")
            
        current_date += timedelta(days=1)
        
    print("Merging data...")
    actual_df = pd.concat(actual_dfs, ignore_index=True) if actual_dfs else pd.DataFrame()
    forecast_df = pd.concat(forecast_dfs, ignore_index=True) if forecast_dfs else pd.DataFrame()
    
    if not actual_df.empty:
        actual_df['startTime'] = pd.to_datetime(actual_df['startTime'], utc=True)
        # BMRS can duplicate rows. Drop duplicates
        actual_df.drop_duplicates(subset=['startTime'], inplace=True)
    
    if not forecast_df.empty:
        forecast_df['startTime'] = pd.to_datetime(forecast_df['startTime'], utc=True)
        forecast_df['publishTime'] = pd.to_datetime(forecast_df['publishTime'], utc=True)
        forecast_df.drop_duplicates(subset=['startTime', 'publishTime'], inplace=True)
        
    print(f"Saving {len(actual_df)} actual records and {len(forecast_df)} forecast records...")
    
    os.makedirs('data', exist_ok=True)
    actual_df.to_csv('data/jan2025_actuals.csv', index=False)
    forecast_df.to_csv('data/jan2025_forecasts.csv', index=False)
    print("Done! Data saved to data/jan2025_actuals.csv and data/jan2025_forecasts.csv")

if __name__ == "__main__":
    fetch_january_data()
