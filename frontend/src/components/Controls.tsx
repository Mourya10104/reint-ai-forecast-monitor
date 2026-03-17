"use client";

import { Calendar, Clock } from "lucide-react";

export default function Controls({
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  horizon,
  setHorizon,
}: any) {
  return (
    <div className="bg-[#111] border border-[#222] rounded-xl p-6 shadow-md flex flex-col md:flex-row gap-8 items-center justify-between">
      
      {/* Date Range Picker */}
      <div className="flex flex-col gap-2 w-full md:w-auto">
        <label className="text-sm font-semibold text-gray-400 flex items-center gap-2 uppercase tracking-wide">
          <Calendar className="w-4 h-4" /> Time Range
        </label>
        <div className="flex gap-4 items-center">
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="bg-[#1a1a1a] border border-[#333] rounded-lg px-4 py-2 text-foreground focus:outline-none focus:border-actual focus:ring-1 focus:ring-actual transition-all"
          />
          <span className="text-gray-500">to</span>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="bg-[#1a1a1a] border border-[#333] rounded-lg px-4 py-2 text-foreground focus:outline-none focus:border-actual focus:ring-1 focus:ring-actual transition-all"
          />
        </div>
      </div>

      {/* Horizon Slider */}
      <div className="flex flex-col gap-2 w-full md:w-1/3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-gray-400 flex items-center gap-2 uppercase tracking-wide">
            <Clock className="w-4 h-4" /> Forecast Horizon
          </label>
          <span className="font-mono text-forecast font-bold">{horizon} Hours</span>
        </div>
        <input
          type="range"
          min="0"
          max="48"
          step="1"
          value={horizon}
          onChange={(e) => setHorizon(parseInt(e.target.value))}
          className="w-full h-2 bg-[#333] rounded-full appearance-none cursor-pointer accent-forecast"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1 font-mono">
          <span>0h</span>
          <span>12h</span>
          <span>24h</span>
          <span>36h</span>
          <span>48h</span>
        </div>
      </div>

    </div>
  );
}
