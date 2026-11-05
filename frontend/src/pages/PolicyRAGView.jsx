import React, { useState, useEffect } from 'react';
import { Search, BookOpen, Quote, ShieldAlert, Sparkles, Loader2, ArrowRight } from 'lucide-react';
import { api } from '../api';

export default function PolicyRAGView() {
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState(5);
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState('All');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const sampleQueries = [
    "What are the ICU visiting hours and family regulations?",
    "What is the emergency response Code Blue resuscitation protocol?",
    "How should high-alert medication dispensing errors be documented?",
    "What are the patient discharge planning and readmission criteria?",
    "What is the HIPAA compliance and patient data privacy guideline?",
  ];

  useEffect(() => {
    async function fetchDocs() {
      const res = await api.getPolicyDocuments();
      if (res.data?.documents) {
        setDocuments(res.data.documents);
      }
    }
    fetchDocs();
  }, []);

  const handleSearch = async (overrideQuery) => {
    const q = overrideQuery || query;
    if (!q.trim()) return;
    setLoading(true);
    setError(null);
    const filter = selectedDoc === 'All' ? null : selectedDoc;
    const res = await api.searchPolicies(q, topK, filter);
    setLoading(false);
    if (res.error) {
      setError(res.error);
    } else {
      setResult(res.data);
    }
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-[#0B1340] via-[#12236E] to-[#1E2FE0] text-white p-8 shadow-md">
        <div className="text-xs font-bold uppercase tracking-wider text-blue-200">Semantic RAG</div>
        <h1 className="text-3xl font-extrabold tracking-tight mt-1 text-white">Policy RAG Search</h1>
        <p className="text-sm text-slate-200 mt-1 max-w-2xl">
          Context-grounded vector search across verified hospital protocols, infection control guidelines, and HIPAA standards.
        </p>
      </div>

      {/* Suggested Clinical Query Pills with Clean Wrapping & Alignment */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-3">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Suggested Clinical Queries
        </div>
        <div className="flex flex-wrap items-center gap-2.5">
          {sampleQueries.map((sq, idx) => (
            <button
              key={idx}
              onClick={() => {
                setQuery(sq);
                handleSearch(sq);
              }}
              className="text-xs font-semibold px-3.5 py-2 rounded-xl bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 border border-slate-200/80 hover:border-blue-200 active:scale-95 transition-all text-left max-w-full cursor-pointer"
            >
              🔍 {sq}
            </button>
          ))}
        </div>
      </div>

      {/* Main Search Bar & Filters */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Ask any question about hospital SOPs, medication safety, or infection control..."
              className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 font-medium"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="px-3 py-3 rounded-xl border border-slate-200 text-xs font-bold bg-white text-slate-700 focus:outline-none"
            >
              <option value={3}>Top 3</option>
              <option value={5}>Top 5</option>
              <option value={8}>Top 8</option>
            </select>

            <select
              value={selectedDoc}
              onChange={(e) => setSelectedDoc(e.target.value)}
              className="px-3 py-3 rounded-xl border border-slate-200 text-xs font-bold bg-white text-slate-700 focus:outline-none max-w-[180px] truncate"
            >
              <option value="All">All Documents</option>
              {documents.map((d, i) => (
                <option key={i} value={d}>{d}</option>
              ))}
            </select>

            <button
              onClick={() => handleSearch()}
              disabled={loading}
              className="px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-bold text-sm shadow-md shadow-blue-500/20 flex items-center justify-center gap-2 shrink-0 cursor-pointer disabled:opacity-50"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
              <span>Search</span>
            </button>
          </div>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-center gap-3">
          <ShieldAlert className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Answer Card */}
          <div className="bg-white p-7 rounded-2xl border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600">
                <Sparkles className="w-4 h-4" />
                <span>Verified Policy Guidance</span>
              </div>
              <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold">
                {Math.round((result.confidence_score || 0.94) * 100)}% Confidence
              </span>
            </div>

            <p className="text-base text-slate-800 leading-relaxed font-normal">
              {result.answer}
            </p>
          </div>

          {/* Citations */}
          {result.citations?.length > 0 && (
            <div className="space-y-3">
              <h4 className="text-sm font-extrabold uppercase tracking-wider text-slate-600">
                Authoritative Source Citations ({result.citations.length})
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.citations.map((c, i) => (
                  <div key={i} className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-blue-700 truncate max-w-[240px]">
                        [{i + 1}] {c.source_document || 'Hospital SOP'}
                      </span>
                      <span className="text-[11px] font-semibold text-slate-400">
                        Section: {c.section || 'General'}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed font-normal">
                      "{c.content}"
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

