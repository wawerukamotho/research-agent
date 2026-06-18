'use client';

import { useState } from 'react';
import ResearchDashboard from "@/components/ResearchDashboard";
import Navigation from "@/components/Navigation";

export default function Home() {
  const [activeTab, setTab] = useState('dashboard');

  return (
    <div className="space-y-8">
      <header className="text-center space-y-4">
        <h2 className="text-3xl font-extrabold text-slate-900 sm:text-4xl">
          Autonomous Research Agent
        </h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Deep investigations, verified claims, and professional reports powered by a multi-agent architecture.
        </p>
      </header>

      <Navigation activeTab={activeTab} setTab={setTab} />

      {activeTab === 'dashboard' && <ResearchDashboard />}
      {activeTab === 'history' && (
        <div className="text-center py-20 bg-white rounded-xl border border-dashed text-slate-400">
          No research history found.
        </div>
      )}
      {activeTab === 'eval' && (
        <div className="text-center py-20 bg-white rounded-xl border border-dashed text-slate-400">
          Evaluation harness dashboard coming soon in Phase 15.
        </div>
      )}
    </div>
  );
}
