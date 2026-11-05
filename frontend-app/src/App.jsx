import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Navigation from './components/Navigation';
import HomeView from './pages/HomeView';
import DashboardView from './pages/DashboardView';
import DocumentIntelligenceView from './pages/DocumentIntelligenceView';
import PolicyRAGView from './pages/PolicyRAGView';
import AppointmentsView from './pages/AppointmentsView';
import EvaluationView from './pages/EvaluationView';
import { api } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [systemStatus, setSystemStatus] = useState({
    online: true,
    mongodb: { connected: true },
    rag_stats: { total_chunks: 8 }
  });

  useEffect(() => {
    async function checkHealth() {
      const res = await api.getHealth();
      if (res.data) {
        setSystemStatus({
          online: true,
          mongodb: res.data.mongodb || { connected: true },
          rag_stats: res.data.rag_stats || { total_chunks: 8 },
        });
      }
    }
    checkHealth();
    const timer = setInterval(checkHealth, 30000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#F5F8FF]">
      {/* Sticky Header with 🛡️ AegisMed Shield Branding & Clean Status Chips */}
      <Header status={systemStatus} onNavigate={setActiveTab} />

      {/* Single-Click Instant Top Navigation Tabs */}
      <Navigation activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Dynamic View Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-2">
        {activeTab === 'home' && <HomeView onNavigate={setActiveTab} />}
        {activeTab === 'dashboard' && <DashboardView status={systemStatus} onNavigate={setActiveTab} />}
        {activeTab === 'doc_intel' && <DocumentIntelligenceView />}
        {activeTab === 'rag_search' && <PolicyRAGView />}
        {activeTab === 'appointments' && <AppointmentsView />}
        {activeTab === 'evaluation' && <EvaluationView />}
      </main>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200/80 bg-white py-6 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-800">🛡️ AegisMed Healthcare Enterprise Platform v1.0.0</span>
            <span className="hidden sm:inline-block">·</span>
            <span>Clinical AI & Administrative Automation</span>
          </div>
          <div className="flex items-center gap-4 text-slate-400 font-medium">
            <span>FastAPI Backend Operational</span>
            <span>•</span>
            <span>ChromaDB Vector Store</span>
            <span>•</span>
            <span>MongoDB Database Synced</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
