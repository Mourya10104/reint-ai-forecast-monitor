import requests
import pandas as pd
from datetime import datetime, timedelta
from fastapi import HTTPException

BMRS_API_BASE = "https://data.elexon.co.uk/bmrs/api/v1"

def fetch_fuelhh(date_str: str) -> pd.DataFrame:
    """Fetch FUELHH data (actual generation by fuel type) and filter for WIND."""
    url = f"{BMRS_API_BASE}/datasets/FUELHH"
    params = {
        "settlementDate": date_str,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch FUELHH at {date_str}: {response.text}")
    
    data = response.json().get('data', [])
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    # Filter for Wind
    df = df[df['fuelType'] == 'WIND']
    if not df.empty:
        df = df[['startTime', 'generation']]
        df.rename(columns={'generation': 'actual_generation'}, inplace=True)
    return df

def fetch_windfor(date_str: str) -> pd.DataFrame:
    """Fetch WINDFOR data (wind forecasts)."""
    url = f"{BMRS_API_BASE}/datasets/WINDFOR"
    params = {
        "settlementDate": date_str,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch WINDFOR at {date_str}: {response.text}")
    
    data = response.json().get('data', [])
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    if not df.empty:
        df = df[['publishTime', 'startTime', 'generation']]
        df.rename(columns={'generation': 'forecasted_generation'}, inplace=True)
    return df

def process_forecast_data(start_date: str, end_date: str, horizon_hours: int) -> list[dict]:
    """
    Fetch and merge actual vs forecasted wind generation data.
    Horizon logic: For a given target startTime T, select the record where 
    publishTime <= T - horizon_hours. Then pick the latest publishTime.
    """
    try:
        s_date = datetime.strptime(start_date, "%Y-%m-%d")
        e_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if (e_date - s_date).days > 7:
         raise HTTPException(status_code=400, detail="Date range cannot exceed 7 days.")
    if e_date < s_date:
         raise HTTPException(status_code=400, detail="End date must be after start date.")

    actual_dfs = []
    forecast_dfs = []

    current_date = s_date
    while current_date <= e_date:
        d_str = current_date.strftime("%Y-%m-%d")
        actual_dfs.append(fetch_fuelhh(d_str))
        forecast_dfs.append(fetch_windfor(d_str))
        current_date += timedelta(days=1)

    actual_df = pd.concat([df for df in actual_dfs if not df.empty], ignore_index=True) if actual_dfs else pd.DataFrame()
    forecast_df = pd.concat([df for df in forecast_dfs if not df.empty], ignore_index=True) if forecast_dfs else pd.DataFrame()

    if actual_df.empty and forecast_df.empty:
        return []

    # Process Forecast Horizon
    if not forecast_df.empty:
        forecast_df['publishTime'] = pd.to_datetime(forecast_df['publishTime'])
        forecast_df['startTime'] = pd.to_datetime(forecast_df['startTime'])

        # Filter: publishTime <= startTime - horizon_hours
        # Equivalently: (startTime - publishTime) >= horizon_hours
        forecast_df['lead_time_hours'] = (forecast_df['startTime'] - forecast_df['publishTime']).dt.total_seconds() / 3600
        filtered_forecast = forecast_df[forecast_df['lead_time_hours'] >= horizon_hours]

        if not filtered_forecast.empty:
            # Pick latest publishTime
            idx = filtered_forecast.groupby('startTime')['publishTime'].idxmax()
            best_forecasts = filtered_forecast.loc[idx]
        else:
            best_forecasts = pd.DataFrame(columns=['startTime', 'forecasted_generation'])
        
        best_forecasts['startTime'] = best_forecasts['startTime'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        best_forecasts = best_forecasts[['startTime', 'forecasted_generation']]
    else:
        best_forecasts = pd.DataFrame(columns=['startTime', 'forecasted_generation'])

    if not actual_df.empty:
        actual_df['startTime'] = pd.to_datetime(actual_df['startTime']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
         actual_df = pd.DataFrame(columns=['startTime', 'actual_generation'])

    # Merge
    if actual_df.empty and best_forecasts.empty:
        merged = pd.DataFrame()
    elif actual_df.empty:
        merged = best_forecasts
    elif best_forecasts.empty:
        merged = actual_df
    else:
        merged = pd.merge(actual_df, best_forecasts, on='startTime', how='outer')

    if not merged.empty:
        merged['startTime_dt'] = pd.to_datetime(merged['startTime'])
        merged.sort_values('startTime_dt', inplace=True)
        merged.drop(columns=['startTime_dt'], inplace=True)
        merged.fillna(value={"actual_generation": None, "forecasted_generation": None}, inplace=True)
        records = merged.to_dict(orient="records")
        import math
        for r in records:
            for k, v in r.items():
                if isinstance(v, float) and math.isnan(v):
                    r[k] = None
        return records
    
    return []
