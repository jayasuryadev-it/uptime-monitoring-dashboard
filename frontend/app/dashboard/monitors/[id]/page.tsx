'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, RefreshCw, ExternalLink, Activity, Percent, Clock, AlertTriangle, Loader2 } from 'lucide-react';
import { apiFetch } from '@/lib/api';
import { getAuthToken } from '@/lib/auth';
import { MonitorDetailResponse } from '@/types';
import ResponseTimeChart from '@/components/ResponseTimeChart';
import HealthCheckHistory from '@/components/HealthCheckHistory';
import IncidentHistory from '@/components/IncidentHistory';
import StatCard from '@/components/StatCard';

export default function MonitorDetailPage() {
  const params = useParams();
  const router = useRouter();
  const monitorId = params.id as string;

  const [detail, setDetail] = useState<MonitorDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDetail = useCallback(async () => {
    try {
      const data = await apiFetch<MonitorDetailResponse>(`/monitors/${monitorId}`);
      setDetail(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load monitor details');
    } finally {
      setLoading(false);
    }
  }, [monitorId]);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.replace('/login');
      return;
    }
    fetchDetail();
  }, [fetchDetail, router]);

  const handleCheckNow = async () => {
    setChecking(true);
    try {
      await apiFetch(`/monitors/${monitorId}/check`, { method: 'POST' });
      await fetchDetail();
    } finally {
      setChecking(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center gap-3 text-slate-600 font-medium">
          <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
          <span>Loading Monitor Details...</span>
        </div>
      </div>
    );
  }

  if (error || !detail) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-12 text-center max-w-lg mx-auto mt-12">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-slate-900 mb-1">Error Loading Monitor</h2>
        <p className="text-sm text-slate-500 mb-6">{error || 'Monitor not found'}</p>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium text-sm hover:bg-blue-700 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const { monitor, uptime_percentage, recent_checks, incidents } = detail;

  return (
    <div className="space-y-8">
      {/* Top Header & Navigation */}
      <div>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 mb-3 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{monitor.name}</h1>
              {monitor.last_status === 'UP' ? (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  OPERATIONAL
                </span>
              ) : monitor.last_status === 'DOWN' ? (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
                  <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                  DOWN
                </span>
              ) : (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 border border-slate-200">
                  UNKNOWN
                </span>
              )}
            </div>
            <a
              href={monitor.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-500 hover:text-blue-600 text-sm mt-1 inline-flex items-center gap-1"
            >
              <span>{monitor.url}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          <button
            onClick={handleCheckNow}
            disabled={checking}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-xl shadow-sm flex items-center gap-2 transition-colors disabled:opacity-50 self-start sm:self-auto"
          >
            <RefreshCw className={`w-4 h-4 ${checking ? 'animate-spin' : ''}`} />
            <span>Check Now</span>
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <StatCard
          title="Uptime Percentage"
          value={`${uptime_percentage}%`}
          icon={<Percent className="w-5 h-5 text-emerald-600" />}
          variant="success"
          subtitle="Based on recent health check probes"
        />
        <StatCard
          title="Latest Response Time"
          value={monitor.last_response_time !== null ? `${monitor.last_response_time} ms` : '—'}
          icon={<Activity className="w-5 h-5 text-blue-600" />}
          subtitle="Ping latency"
        />
        <StatCard
          title="Check Configuration"
          value={`Every ${monitor.interval}s`}
          icon={<Clock className="w-5 h-5 text-slate-600" />}
          subtitle={`Timeout: ${monitor.timeout}s`}
        />
      </div>

      {/* Response Time Graph */}
      <ResponseTimeChart checks={recent_checks} />

      {/* Health Check History & Incident History */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <HealthCheckHistory checks={recent_checks} />
        </div>
        <div className="lg:col-span-1">
          <IncidentHistory incidents={incidents} />
        </div>
      </div>
    </div>
  );
}
