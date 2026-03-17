"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { format } from 'date-fns';

export default function WindChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center text-gray-500">
        <p>No data available for the selected range.</p>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const actual = payload.find((p: any) => p.dataKey === 'actual_generation')?.value;
      const forecast = payload.find((p: any) => p.dataKey === 'forecasted_generation')?.value;
      const delta = (forecast !== undefined && actual !== undefined) ? forecast - actual : 'N/A';
      
      return (
        <div className="bg-[#1a1a1a] border border-[#333] p-4 rounded-lg shadow-xl text-sm">
          <p className="font-semibold text-gray-300 mb-2">
            {format(new Date(label), "MMM dd, HH:mm")}
          </p>
          {actual !== undefined && (
            <p style={{ color: "var(--color-actual)" }}>
              Actual: {actual.toFixed(2)} MW
            </p>
          )}
          {forecast !== undefined && (
            <p style={{ color: "var(--color-forecast)" }}>
              Forecast: {forecast.toFixed(2)} MW
            </p>
          )}
          {delta !== 'N/A' && (
            <p className="mt-2 pt-2 border-t border-[#333] text-gray-400">
              <span className="font-semibold">Delta (Error): </span>
              <span className={delta > 0 ? "text-red-400" : "text-green-400"}>
                {delta > 0 ? "+" : ""}{delta.toFixed(2)} MW
              </span>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
        <XAxis 
          dataKey="startTime" 
          stroke="#888" 
          tickFormatter={(tick) => format(new Date(tick), "dd MMM")} 
          tickMargin={10}
        />
        <YAxis 
          stroke="#888" 
          tickFormatter={(value) => `${value}MW`}
          tickMargin={10}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ paddingTop: "20px" }} />
        
        <Line 
          type="monotone" 
          name="Actual Wind Generation"
          dataKey="actual_generation" 
          stroke="var(--color-actual)" 
          strokeWidth={3}
          dot={false}
          activeDot={{ r: 6 }}
        />
        <Line 
          type="monotone" 
          name="Forecasted Wind Generation"
          dataKey="forecasted_generation" 
          stroke="var(--color-forecast)" 
          strokeWidth={3}
          dot={false}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
