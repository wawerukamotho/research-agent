'use client';

import { useState } from 'react';
import { api, ResearchStatus } from '@/lib/api';
import { Search, Loader2, FileText, FileCode, FileType } from 'lucide-react';
import AgentTraceViewer from './AgentTraceViewer';

export default function ResearchDashboard() {
  const [query, setQuery] = useState('');
  const [session, setSession] = useState<ResearchStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStartResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setError(null);
    try {
      const res = await api.startResearch({ query });
      setSession(res);
      startEventStream(res.session_id);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to start research');
    } finally {
      setLoading(false);
    }
  };

  const startEventStream = (sessionId: string) => {
    const eventSource = api.getEventSource(sessionId);

    eventSource.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      if (parsed.event === 'progress') {
        setSession(parsed.data);
      } else if (parsed.event === 'completed') {
        setSession(prev => prev ? { ...prev, status: 'finished' } : null);
        eventSource.close();
      }
    };

    eventSource.onerror = () => {
      eventSource.close();
    };
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Search Input */}
      <section className="bg-white p-6 rounded-xl border shadow-sm">
        <form onSubmit={handleStartResearch} className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="What do you want to research?"
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-900"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2 transition-colors"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Start Research"}
          </button>
        </form>
        {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}
      </section>

      {/* Execution Progress */}
      {session && (
        <section className="bg-white p-6 rounded-xl border shadow-sm space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-slate-900">Research Status</h2>
            <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
              session.status === 'finished' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
            }`}>
              {session.status}
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm text-slate-500">
              <span>Progress</span>
              <span>{Math.round(session.progress * 100)}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${session.progress * 100}%` }}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-xs text-slate-400 block mb-1 uppercase font-bold">Steps Executed</span>
              <span className="text-2xl font-mono text-slate-700">{session.step_count}</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-xs text-slate-400 block mb-1 uppercase font-bold">Current Task</span>
              <span className="text-sm font-medium text-slate-700 line-clamp-1">{session.current_task || 'N/A'}</span>
            </div>
          </div>

          <AgentTraceViewer session={session} />

          {session.status === 'finished' && (
            <div className="pt-6 border-t flex flex-wrap gap-4">
              <a href={api.getDownloadUrl(session.session_id, 'pdf')} className="flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600 transition-colors">
                <FileText className="w-4 h-4" /> Download PDF
              </a>
              <a href={api.getDownloadUrl(session.session_id, 'md')} className="flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600 transition-colors">
                <FileCode className="w-4 h-4" /> Download Markdown
              </a>
              <a href={api.getDownloadUrl(session.session_id, 'docx')} className="flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600 transition-colors">
                <FileType className="w-4 h-4" /> Download DOCX
              </a>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
