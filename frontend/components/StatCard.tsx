'use client';

import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  subtitle?: string;
  variant?: 'default' | 'success' | 'danger' | 'warning';
}

export default function StatCard({ title, value, icon, subtitle, variant = 'default' }: StatCardProps) {
  const getBadgeStyle = () => {
    switch (variant) {
      case 'success':
        return 'bg-emerald-50 border-emerald-100 text-emerald-600';
      case 'danger':
        return 'bg-rose-50 border-rose-100 text-rose-600';
      case 'warning':
        return 'bg-amber-50 border-amber-100 text-amber-600';
      default:
        return 'bg-blue-50 border-blue-100 text-blue-600';
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-500">{title}</span>
        <div className={`p-2.5 rounded-lg border ${getBadgeStyle()}`}>
          {icon}
        </div>
      </div>
      <div className="mt-3">
        <div className="text-2xl sm:text-3xl font-bold text-slate-900">{value}</div>
        {subtitle && <div className="text-xs text-slate-500 mt-1">{subtitle}</div>}
      </div>
    </div>
  );
}
