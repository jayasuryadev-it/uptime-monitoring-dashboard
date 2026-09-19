import './globals.css';
import React from 'react';
import Navbar from '@/components/Navbar';

export const metadata = {
  title: 'PulseWatch - Uptime Monitoring Dashboard',
  description: 'Real-time website and API health monitoring dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500">
          PulseWatch Uptime Monitor &copy; {new Date().getFullYear()} — Baseline Local Version
        </footer>
      </body>
    </html>
  );
}
