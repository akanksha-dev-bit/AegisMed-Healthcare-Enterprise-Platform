import React from 'react';
import { Home, BarChart3, FileText, Search, Calendar, CheckSquare } from 'lucide-react';

export default function Navigation({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'doc_intel', label: 'Document Intelligence', icon: FileText },
    { id: 'rag_search', label: 'Policy RAG Search', icon: Search },
    { id: 'appointments', label: 'Appointments', icon: Calendar },
    { id: 'evaluation', label: 'AI Evaluation', icon: CheckSquare },
  ];

  return (
    <nav className="w-full py-4 px-4 sm:px-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white/90 p-1.5 rounded-full border border-slate-200/90 shadow-sm shadow-blue-500/5 flex items-center justify-between sm:justify-center gap-1 overflow-x-auto custom-scrollbar">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                type="button"
                className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs sm:text-sm font-bold transition-all duration-200 whitespace-nowrap cursor-pointer select-none ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                    : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50/80 active:scale-95'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-blue-600'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
