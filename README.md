# REInt AI Forecast Monitor

A sophisticated dashboard to monitor and compare actual wind generation vs. forecasted wind generation in the UK energy market using the Elexon BMRS Insights API.

## Project Structure

This project consists of:
1. **Backend**: Python 3.12+ FastAPI application serving processed time-series data.
2. **Frontend**: React (Next.js 14+) with Tailwind CSS representing the "Clean Dark" UI.

## Data Processing Logic

The core logic (The "Rigor" Layer) sits in the backend (`backend/data_engine.py`):
- Fetch **Actuals (`FUELHH`)** where `fuelType == "WIND"`.
- Fetch **Forecasts (`WINDFOR`)**.
- Filter Forecasts by the **Forecast Horizon**: Only selects forecast records where the time it was published (`publishTime`) is at or before the target time minus the horizon (`publishTime <= startTime - horizon_hours`).
- Among the valid forecasts for a target time, it selects the **latest available forecast** (most recent knowledge).

## Architectural Trade-Offs

1. **Backend API Parsing vs DB Storage**:
   - *Trade-off*: Currently, the backend fetches data on-the-fly from the BMRS API for the requested date range instead of storing it in a local database (like PostgreSQL/TimescaleDB).
   - *Reasoning*: For a lightweight monitor or POC, passing through to the external API prevents the need for background cron jobs or ETL pipelines.
   - *Consideration*: If the date range is massive, this can be slow due to the 7-day restriction on BMRS sets and pagination. A long-term production app would ingest BMRS data into a time-series DB.

2. **Handling Missing Data (NaN Substitution)**:
   - *Trade-off*: When merging DataFrames, some `startTime` buckets may have forecasts but lack actuals (or vice-versa).
   - *Reasoning*: Pandas uses `NaN` which is non-serializable in JSON. The engine replaces `NaN` with Python `None` (JSON `null`). The frontend (`Recharts`) is configured to handle missing data points by interpolating or breaking the line cleanly, rather than failing to render.

3. **Frontend Client-Side Fetching vs Server Components**:
   - *Trade-off*: The main Dashboard component is marked with `"use client"` and fetches data using a standard `useEffect` hook. Next.js App Router allows Server Components.
   - *Reasoning*: Because the dashboard relies heavily on user interaction (changing the Date Range or the Horizon slider), the data is highly dynamic. Client-side fetching allows immediate refetch without a full page reload or complex server-action piping for simple state changes.

## Running Locally

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:3000`.
