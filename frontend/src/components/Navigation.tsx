'use client';

import { BarChart3, Clock, LayoutDashboard } from 'lucide-react';

export default function Navigation({ activeTab, setTab }: { activeTab: string, setTab: (t: string) => void }) {
  return (
    <nav className="flex gap-4 border-b mb-8">
      <button
        onClick={() => setTab('dashboard')}
        className={`px-4 py-2 flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'dashboard' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
      >
        <LayoutDashboard className="w-4 h-4" /> Dashboard
      </button>
      <button
        onClick={() => setTab('history')}
        className={`px-4 py-2 flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'history' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
      >
        <Clock className="w-4 h-4" /> History
      </button>
      <button
        onClick={() => setTab('eval')}
        className={`px-4 py-2 flex items-center gap-2 border-b-2 transition-colors ${activeTab === 'eval' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
      >
        <BarChart3 className="w-4 h-4" /> Evaluation
      </button>
    </nav>
  );
}
