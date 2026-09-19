'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Play, Pause, RefreshCw, Edit2, Trash2, ExternalLink, ArrowRight, Clock, AlertTriangle } from 'lucide-react';
import { Monitor } from '@/types';

interface MonitorListProps {
  monitors: Monitor[];
  onToggleActive: (id: string) => Promise<void>;
  onCheckNow: (id: string) => Promise<void>;
  onEdit: (monitor: Monitor) => void;
  onDelete: (id: string) => Promise<void>;
}

export default function MonitorList({
  monitors,
  onToggleActive,
  onCheckNow,
  onEdit,
  onDelete,
}: MonitorListProps) {
  const [checkingIds, setCheckingIds] = useState<Record<string, boolean>>({});

  const handleCheckNow = async (id: string) => {
    setCheckingIds((prev) => ({ ...prev, [id]: true }));
    try {
      await onCheckNow(id);
    } finally {
      setCheckingIds((prev) => ({ ...prev, [id]: false }));
    }
  };

  if (monitors.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
        <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <Clock className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-semibold text-slate-900 mb-1">No Monitors Added Yet</h3>
        <p className="text-slate-500 text-sm max-w-sm mx-auto mb-6">
          Start tracking your web applications and API endpoints by adding your first uptime monitor.
        </p>
      </div>
    );
  }

  const renderStatusBadge = (monitor: Monitor) => {
    if (!monitor.is_active) {
      return (
        <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
          PAUSED
        </span>
      );
    }
    if (monitor.last_status === 'UP') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          UP
        </span>
      );
    }
    if (monitor.last_status === 'DOWN') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
          DOWN
        </span>
      );
    }
    return (
      <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
        UNKNOWN
      </span>
    );
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="py-3.5 px-6">Monitor</th>
              <th className="py-3.5 px-4">Status</th>
              <th className="py-3.5 px-4">Response Time</th>
              <th className="py-3.5 px-4">Interval</th>
              <th className="py-3.5 px-4">Last Checked</th>
              <th className="py-3.5 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {monitors.map((m) => (
              <tr key={m.id} className="hover:bg-slate-50/80 transition-colors">
                <td className="py-4 px-6">
                  <div className="flex flex-col">
                    <Link
                      href={`/dashboard/monitors/${m.id}`}
                      className="font-semibold text-slate-900 hover:text-blue-600 flex items-center gap-1.5 group"
                    >
                      <span>{m.name}</span>
                      <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all text-blue-600" />
                    </Link>
                    <a
                      href={m.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-slate-500 hover:underline flex items-center gap-1 mt-0.5 truncate max-w-xs"
                    >
                      <span className="truncate">{m.url}</span>
                      <ExternalLink className="w-3 h-3 flex-shrink-0" />
                    </a>
                  </div>
                </td>
                <td className="py-4 px-4 whitespace-nowrap">
                  {renderStatusBadge(m)}
                </td>
                <td className="py-4 px-4 whitespace-nowrap">
                  {m.last_response_time !== null && m.last_response_time !== undefined ? (
                    <span className="font-mono text-xs font-medium text-slate-700 bg-slate-100 px-2 py-1 rounded">
                      {m.last_response_time} ms
                    </span>
                  ) : (
                    <span className="text-slate-400 text-xs">—</span>
                  )}
                </td>
                <td className="py-4 px-4 whitespace-nowrap text-slate-600 text-xs">
                  every {m.interval}s
                </td>
                <td className="py-4 px-4 whitespace-nowrap text-slate-500 text-xs">
                  {m.last_checked_at
                    ? new Date(m.last_checked_at).toLocaleTimeString()
                    : 'Never'}
                </td>
                <td className="py-4 px-6 whitespace-nowrap text-right">
                  <div className="flex items-center justify-end gap-1.5">
                    <button
                      onClick={() => handleCheckNow(m.id)}
                      disabled={checkingIds[m.id]}
                      title="Run Health Check Now"
                      className="p-1.5 rounded-lg text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition-colors disabled:opacity-50"
                    >
                      <RefreshCw className={`w-4 h-4 ${checkingIds[m.id] ? 'animate-spin text-blue-600' : ''}`} />
                    </button>
                    <button
                      onClick={() => onToggleActive(m.id)}
                      title={m.is_active ? 'Pause Monitor' : 'Enable Monitor'}
                      className={`p-1.5 rounded-lg transition-colors ${
                        m.is_active
                          ? 'text-slate-500 hover:text-amber-600 hover:bg-amber-50'
                          : 'text-emerald-600 hover:bg-emerald-50'
                      }`}
                    >
                      {m.is_active ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => onEdit(m)}
                      title="Edit Monitor"
                      className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(m.id)}
                      title="Delete Monitor"
                      className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
