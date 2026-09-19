'use client';

import React from 'react';
import { HealthCheck } from '@/types';

interface ResponseTimeChartProps {
  checks: HealthCheck[];
}

export default function ResponseTimeChart({ checks }: ResponseTimeChartProps) {
  if (checks.length === 0) return null;

  // Take up to last 20 checks reversed so chronological left -> right
  const chronologicalChecks = [...checks].slice(0, 20).reverse();
  const maxMs = Math.max(...chronologicalChecks.map((c) => c.response_time), 100);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-semibold text-slate-900 text-base">Response Time Latency</h3>
          <p className="text-xs text-slate-500">Ping latency trend over recent probes (ms)</p>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400">Peak Latency: </span>
          <span className="text-sm font-bold font-mono text-slate-800">{maxMs.toFixed(0)} ms</span>
        </div>
      </div>

      <div className="h-32 w-full flex items-end gap-1.5 pt-4 border-b border-slate-200">
        {chronologicalChecks.map((c, i) => {
          const heightPct = Math.max((c.response_time / maxMs) * 100, 8);
          const isUp = c.status === 'UP';
          return (
            <div
              key={c.id || i}
              className="flex-1 flex flex-col items-center group relative h-full justify-end"
            >
              {/* Tooltip */}
              <div className="absolute bottom-full mb-2 hidden group-hover:flex flex-col items-center z-20 pointer-events-none">
                <div className="bg-slate-900 text-white text-xs py-1 px-2.5 rounded shadow-lg whitespace-nowrap font-mono">
                  {c.response_time} ms ({c.status})
                  <div className="text-[10px] text-slate-400">
                    {new Date(c.checked_at).toLocaleTimeString()}
                  </div>
                </div>
                <div className="w-2 h-2 bg-slate-900 rotate-45 -mt-1"></div>
              </div>

              <div
                style={{ height: `${heightPct}%` }}
                className={`w-full rounded-t transition-all ${
                  isUp
                    ? 'bg-blue-500 group-hover:bg-blue-600'
                    : 'bg-rose-500 group-hover:bg-rose-600'
                }`}
              />
            </div>
          );
        })}
      </div>
      <div className="flex justify-between text-[11px] text-slate-400 mt-2 font-mono">
        <span>Oldest</span>
        <span>Latest ({chronologicalChecks[chronologicalChecks.length - 1]?.response_time || 0} ms)</span>
      </div>
    </div>
  );
}
