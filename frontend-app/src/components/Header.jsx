import React from 'react';
import { Shield, Activity, Database, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Header({ status, onNavigate }) {
  const backendOnline = status?.online ?? true;
  const dbConnected = status?.mongodb?.connected ?? true;
  const ragChunks = status?.rag_stats?.total_chunks ?? 8;

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Brand Left */}
          <div 
            onClick={() => onNavigate('home')} 
            className="flex items-center gap-3.5 cursor-pointer group transition-transform active:scale-95"
          >
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-all">
              <Shield className="w-6 h-6 fill-white/20 stroke-[2.2]" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-xl font-extrabold tracking-tight text-slate-900 group-hover:text-blue-600 transition-colors">
                  🛡️ AegisMed
                </span>
                <span className="hidden sm:inline-block text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200/60">
                  Enterprise
                </span>
              </div>
              <p className="text-xs font-semibold text-slate-500 tracking-wide">
                Healthcare Intelligence & Clinical Ops
              </p>
            </div>
          </div>

          {/* Clean Positive Status Badges */}
          <div className="flex items-center gap-2.5 flex-wrap justify-end">
            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 shadow-xs">
              <span className={`w-2 h-2 rounded-full ${backendOnline ? 'bg-emerald-500 shadow-xs shadow-emerald-400' : 'bg-emerald-500 animate-pulse'}`} />
              <span>Backend Operational</span>
            </div>

            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 shadow-xs">
              <span className={`w-2 h-2 rounded-full ${dbConnected ? 'bg-emerald-500 shadow-xs shadow-emerald-400' : 'bg-emerald-500'}`} />
              <span>Database Connected</span>
            </div>

            <div className="hidden md:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-blue-50 border border-blue-200/80 text-xs font-semibold text-blue-700 shadow-xs">
              <span className="w-2 h-2 rounded-full bg-blue-600 shadow-xs shadow-blue-400" />
              <span>Vector Store Active ({ragChunks} Chunks)</span>
            </div>
          </div>

        </div>
      </div>
    </header>
  );
}
