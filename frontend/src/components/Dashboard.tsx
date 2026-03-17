"use client";

import { useState, useEffect } from "react";
import Dashboard from "./Dashboard";
import WindChart from "./WindChart";
import Controls from "./Controls";
import { format, subDays } from "date-fns";
import { Loader2, AlertCircle } from "lucide-react";

type DataPoint = {
  startTime: str;
  actual_generation: number | null;
  forecasted_generation: number | null;
  [key: string]: any; // Allow computed fields like delta
};

export default function DashboardComponent() {
  // Setup default: last 7 days of Jan 2025
  const [startDate, setStartDate] = useState("2025-01-25");
  const [endDate, setEndDate] = useState("2025-01-31");
  const [horizon, setHorizon] = useState(24);
  const [data, setData] = useState<DataPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `http://localhost:8000/api/monitor?start_date=${startDate}&end_date=${endDate}&horizon_hours=${horizon}`
      );
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const json = await response.json();
      
      // Compute Delta (Error) = Forecast - Actual for the tooltip
      const processedData = json.data.map((d: any) => ({
        ...d,
        delta: (d.forecasted_generation !== null && d.actual_generation !== null)
          ? d.forecasted_generation - d.actual_generation
          : null
      }));

      setData(processedData || []);
    } catch (err: any) {
      setError(err.message || "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  };

  // Re-fetch when dependencies change
  useEffect(() => {
    fetchData();
  }, [startDate, endDate, horizon]);

  return (
    <div className="space-y-6">
      <Controls 
        startDate={startDate} setStartDate={setStartDate}
        endDate={endDate} setEndDate={setEndDate}
        horizon={horizon} setHorizon={setHorizon}
      />
      
      <div className="bg-[#111] border border-[#222] rounded-xl p-6 shadow-2xl relative">
        {loading && (
          <div className="absolute inset-0 bg-[#0a0a0ae6] flex items-center justify-center rounded-xl z-10 transition-opacity">
            <Loader2 className="w-8 h-8 animate-spin text-actual" />
          </div>
        )}
        
        {error ? (
          <div className="flex flex-col items-center justify-center py-20 text-red-400">
            <AlertCircle className="w-12 h-12 mb-4 opacity-50" />
            <p>{error}</p>
          </div>
        ) : (
          <div className="h-[500px] w-full">
            <WindChart data={data} />
          </div>
        )}
      </div>
    </div>
  );
}
