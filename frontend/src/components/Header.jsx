import React from 'react';
import {
  Shield,
  Home,
  BarChart3,
  FileText,
  Search,
  Calendar,
  CheckSquare
} from 'lucide-react';

export default function Header({ activeTab, onTabChange, status }) {
  const backendOnline = status?.online ?? true;
  const dbConnected = status?.mongodb?.connected ?? true;
  const ragChunks = status?.rag_stats?.total_chunks ?? 8;

  const navItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'doc_intel', label: 'Document Intelligence', icon: FileText },
    { id: 'rag_search', label: 'Policy RAG Search', icon: Search },
    { id: 'appointments', label: 'Appointments', icon: Calendar },
    { id: 'evaluation', label: 'AI Evaluation', icon: CheckSquare },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 px-4 sm:px-6 py-3 shadow-xs">
      <div className="max-w-[1440px] mx-auto flex items-center justify-between gap-4">

        {/* LEFT: Logo & Brand */}
        <div
          onClick={() => onTabChange('home')}
          className="flex items-center gap-3 cursor-pointer select-none shrink-0 group transition-transform active:scale-95"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-all">
            <Shield className="w-5 h-5 fill-white/20 stroke-[2.4]" />
          </div>
          <div>
            <div className="flex items-center gap-1.5 leading-none">
              <span className="text-lg font-black tracking-tight text-slate-900 group-hover:text-blue-600 transition-colors">
                🛡️ AegisMed
              </span>
              <span className="text-[10px] font-extrabold uppercase tracking-widest px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200/80">
                ENTERPRISE
              </span>
            </div>
            <p className="text-[11px] font-semibold text-slate-400 tracking-tight mt-0.5">
              Healthcare Intelligence Platform
            </p>
          </div>
        </div>

        {/* CENTER: Navigation Tabs directly inside Header */}
        <nav className="hidden lg:flex items-center gap-1 bg-slate-50/90 p-1.5 rounded-full border border-slate-200/80 shadow-inner">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                type="button"
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-bold transition-all duration-150 whitespace-nowrap cursor-pointer select-none ${isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/25'
                    : 'text-slate-600 hover:text-blue-600 hover:bg-white active:scale-95'
                  }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-blue-600'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>



      </div>

      {/* Mobile/Tablet Fallback Navigation Bar below Header on small screens only */}
      <div className="lg:hidden mt-2 pt-2 border-t border-slate-100 flex items-center gap-1 overflow-x-auto custom-scrollbar pb-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              type="button"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${isActive
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-100'
                }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
