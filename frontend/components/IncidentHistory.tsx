'use client';

import React from 'react';
import { AlertCircle, CheckCircle2, Clock } from 'lucide-react';
import { Incident } from '@/types';

interface IncidentHistoryProps {
  incidents: Incident[];
}

export default function IncidentHistory({ incidents }: IncidentHistoryProps) {
  if (incidents.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-slate-500 text-sm">
        <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2 opacity-80" />
        No downtime incidents recorded. Monitor is running smoothly!
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/50 flex items-center justify-between">
        <h3 className="font-semibold text-slate-900 text-base">Incident Log</h3>
        <span className="text-xs text-slate-500 font-medium">{incidents.length} incidents recorded</span>
      </div>
      <div className="p-6">
        <div className="relative pl-6 border-l-2 border-slate-200 space-y-6">
          {incidents.map((inc) => {
            const isResolved = Boolean(inc.resolved_at);
            return (
              <div key={inc.id} className="relative group">
                <div className={`absolute -left-[31px] top-0.5 w-4 h-4 rounded-full border-2 bg-white ${
                  isResolved ? 'border-emerald-500' : 'border-rose-500 animate-ping'
                }`} />
                <div className={`absolute -left-[31px] top-0.5 w-4 h-4 rounded-full border-2 bg-white ${
                  isResolved ? 'border-emerald-500' : 'border-rose-500'
                }`} />

                <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${
                      isResolved
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}>
                      {isResolved ? 'RESOLVED' : 'ACTIVE INCIDENT'}
                    </span>
                    <span className="text-xs text-slate-500 font-mono">
                      {new Date(inc.started_at).toLocaleString()}
                    </span>
                  </div>

                  <p className="text-sm font-medium text-slate-900 mt-2">
                    {inc.reason}
                  </p>

                  <div className="mt-2 text-xs text-slate-500 flex items-center gap-4">
                    <span>Started: {new Date(inc.started_at).toLocaleTimeString()}</span>
                    {isResolved && (
                      <span>
                        Resolved: {new Date(inc.resolved_at!).toLocaleTimeString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
