'use client';

import { ResearchStatus } from '@/lib/api';
import { History, Activity, Database, CheckSquare } from 'lucide-react';

export default function AgentTraceViewer({ session }: { session: ResearchStatus }) {
  // In a real app, this would fetch detailed tool history from the backend.
  // For Phase 12, we visualize based on current session progress.

  return (
    <div className="bg-white p-6 rounded-xl border shadow-sm space-y-4">
      <div className="flex items-center gap-2 border-b pb-4">
        <Activity className="w-5 h-5 text-blue-600" />
        <h2 className="text-lg font-semibold text-slate-900">Execution Trace</h2>
      </div>

      <div className="space-y-4">
        <div className="flex gap-4 items-start">
          <div className="mt-1 bg-green-100 p-2 rounded-full">
            <CheckSquare className="w-4 h-4 text-green-600" />
          </div>
          <div>
            <p className="text-sm font-bold text-slate-700 uppercase tracking-tight text-[10px]">Plan Initialized</p>
            <p className="text-xs text-slate-500">Research plan generated for: {session.query}</p>
          </div>
        </div>

        {session.step_count > 0 && (
          <div className="flex gap-4 items-start">
            <div className="mt-1 bg-blue-100 p-2 rounded-full">
              <Database className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-700 uppercase tracking-tight text-[10px]">Data Collection</p>
              <p className="text-xs text-slate-500">Executed {session.step_count} research tools in parallel.</p>
            </div>
          </div>
        )}

        {session.status === 'finished' && (
          <div className="flex gap-4 items-start animate-in fade-in slide-in-from-top-2">
            <div className="mt-1 bg-purple-100 p-2 rounded-full">
              <History className="w-4 h-4 text-purple-600" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-700 uppercase tracking-tight text-[10px]">Synthesis Complete</p>
              <p className="text-xs text-slate-500">Final report generated and validated by subagents.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
