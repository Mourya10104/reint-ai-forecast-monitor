from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from data_engine import process_forecast_data

app = FastAPI(title="Forecast Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/monitor")
def get_monitor_data(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    horizon_hours: int = Query(24, description="Forecast Horizon in hours", ge=0, le=48)
):
    """
    Get merged actual vs forecasted wind generation data.
    Horizon logic applies filtering based on lead time.
    """
    data = process_forecast_data(start_date, end_date, horizon_hours)
    return {"data": data}
