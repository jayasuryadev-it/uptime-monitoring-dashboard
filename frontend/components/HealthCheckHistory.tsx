'use client';

import React from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';
import { HealthCheck } from '@/types';

interface HealthCheckHistoryProps {
  checks: HealthCheck[];
}

export default function HealthCheckHistory({ checks }: HealthCheckHistoryProps) {
  if (checks.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-slate-500 text-sm">
        No health checks recorded yet. Click "Check Now" to trigger the first probe.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/50 flex items-center justify-between">
        <h3 className="font-semibold text-slate-900 text-base">Recent Health Checks</h3>
        <span className="text-xs text-slate-500 font-medium">Last {checks.length} checks</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-sm">
          <thead>
            <tr className="bg-slate-50/50 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
              <th className="py-3 px-6">Status</th>
              <th className="py-3 px-4">Status Code</th>
              <th className="py-3 px-4">Response Time</th>
              <th className="py-3 px-4">Timestamp</th>
              <th className="py-3 px-6">Details / Errors</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {checks.map((check) => (
              <tr key={check.id} className="hover:bg-slate-50/60 transition-colors">
                <td className="py-3.5 px-6 whitespace-nowrap">
                  {check.status === 'UP' ? (
                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                      UP
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-0.5 rounded-full">
                      <XCircle className="w-3.5 h-3.5 text-rose-600" />
                      DOWN
                    </span>
                  )}
                </td>
                <td className="py-3.5 px-4 whitespace-nowrap">
                  {check.status_code ? (
                    <span className={`font-mono text-xs font-medium px-2 py-0.5 rounded ${
                      check.status_code >= 200 && check.status_code < 400
                        ? 'bg-slate-100 text-slate-700'
                        : 'bg-rose-100 text-rose-800'
                    }`}>
                      {check.status_code}
                    </span>
                  ) : (
                    <span className="text-slate-400 text-xs">—</span>
                  )}
                </td>
                <td className="py-3.5 px-4 whitespace-nowrap font-mono text-xs text-slate-700">
                  {check.response_time} ms
                </td>
                <td className="py-3.5 px-4 whitespace-nowrap text-xs text-slate-500">
                  {new Date(check.checked_at).toLocaleString()}
                </td>
                <td className="py-3.5 px-6 text-xs text-slate-600 max-w-md truncate">
                  {check.error_message ? (
                    <span className="text-rose-600 font-medium">{check.error_message}</span>
                  ) : (
                    <span className="text-slate-400">Normal HTTP 200 OK response</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
