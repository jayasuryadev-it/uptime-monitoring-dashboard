'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Plus, Activity, CheckCircle2, AlertTriangle, PauseCircle, Percent, RefreshCw, Loader2, Search } from 'lucide-react';
import { apiFetch } from '@/lib/api';
import { getAuthToken } from '@/lib/auth';
import { DashboardSummary, Monitor } from '@/types';
import StatCard from '@/components/StatCard';
import MonitorList from '@/components/MonitorList';
import MonitorModal from '@/components/MonitorModal';

export default function DashboardPage() {
  const router = useRouter();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'UP' | 'DOWN' | 'PAUSED'>('ALL');

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingMonitor, setEditingMonitor] = useState<Monitor | null>(null);

  const fetchDashboardData = useCallback(async (showRefreshing = false) => {
    if (showRefreshing) setRefreshing(true);
    try {
      const data = await apiFetch<DashboardSummary>('/dashboard/summary');
      setSummary(data);
    } catch (err) {
      // Error handled by apiFetch redirect
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    const token = getAuthToken();
    if (!token) {
      router.replace('/login');
      return;
    }
    fetchDashboardData();

    // Auto-poll dashboard stats every 15 seconds
    const interval = setInterval(() => {
      fetchDashboardData(false);
    }, 15000);

    return () => clearInterval(interval);
  }, [fetchDashboardData, router]);

  const handleCreateOrUpdateMonitor = async (data: { name: string; url: string; interval: number; timeout: number }) => {
    if (editingMonitor) {
      await apiFetch(`/monitors/${editingMonitor.id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      });
    } else {
      await apiFetch('/monitors', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    }
    await fetchDashboardData(true);
  };

  const handleToggleActive = async (id: string) => {
    await apiFetch(`/monitors/${id}/toggle`, { method: 'PATCH' });
    await fetchDashboardData(true);
  };

  const handleCheckNow = async (id: string) => {
    await apiFetch(`/monitors/${id}/check`, { method: 'POST' });
    await fetchDashboardData(true);
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this monitor?')) {
      await apiFetch(`/monitors/${id}`, { method: 'DELETE' });
      await fetchDashboardData(true);
    }
  };

  const openCreateModal = () => {
    setEditingMonitor(null);
    setIsModalOpen(true);
  };

  const openEditModal = (monitor: Monitor) => {
    setEditingMonitor(monitor);
    setIsModalOpen(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex items-center gap-3 text-slate-600 font-medium">
          <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
          <span>Loading Dashboard...</span>
        </div>
      </div>
    );
  }

  const filteredMonitors = (summary?.monitors || []).filter((m) => {
    const matchesSearch =
      m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.url.toLowerCase().includes(searchQuery.toLowerCase());
    if (!matchesSearch) return false;

    if (statusFilter === 'UP') return m.is_active && m.last_status === 'UP';
    if (statusFilter === 'DOWN') return m.is_active && m.last_status === 'DOWN';
    if (statusFilter === 'PAUSED') return !m.is_active;
    return true;
  });

  return (
    <div className="space-y-8">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">System Overview</h1>
          <p className="text-slate-500 text-sm mt-0.5">Live status and uptime metrics across all services</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => fetchDashboardData(true)}
            disabled={refreshing}
            className="p-2.5 text-slate-600 hover:text-blue-600 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl shadow-sm transition-colors disabled:opacity-50"
            title="Refresh Stats"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin text-blue-600' : ''}`} />
          </button>
          <button
            onClick={openCreateModal}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-xl shadow-sm flex items-center gap-2 transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Add Monitor</span>
          </button>
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Total Monitors"
          value={summary?.total_monitors || 0}
          icon={<Activity className="w-5 h-5 text-blue-600" />}
          subtitle="Monitored endpoints"
        />
        <StatCard
          title="Monitors UP"
          value={summary?.up_monitors || 0}
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-600" />}
          variant="success"
          subtitle="Operational"
        />
        <StatCard
          title="Monitors DOWN"
          value={summary?.down_monitors || 0}
          icon={<AlertTriangle className="w-5 h-5 text-rose-600" />}
          variant={summary?.down_monitors ? 'danger' : 'default'}
          subtitle="Require attention"
        />
        <StatCard
          title="Overall Uptime"
          value={`${summary?.overall_uptime_percentage || 100}%`}
          icon={<Percent className="w-5 h-5 text-emerald-600" />}
          variant="success"
          subtitle="Historical uptime average"
        />
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search monitor name or URL..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white"
          />
        </div>

        <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          {(['ALL', 'UP', 'DOWN', 'PAUSED'] as const).map((filter) => (
            <button
              key={filter}
              onClick={() => setStatusFilter(filter)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                statusFilter === filter
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* Monitor List Table */}
      <MonitorList
        monitors={filteredMonitors}
        onToggleActive={handleToggleActive}
        onCheckNow={handleCheckNow}
        onEdit={openEditModal}
        onDelete={handleDelete}
      />

      {/* Create / Edit Modal */}
      <MonitorModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateOrUpdateMonitor}
        initialData={editingMonitor}
        title={editingMonitor ? 'Edit Monitor' : 'Create New Monitor'}
      />
    </div>
  );
}
