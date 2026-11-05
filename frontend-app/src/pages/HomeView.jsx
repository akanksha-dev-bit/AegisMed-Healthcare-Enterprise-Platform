import React from 'react';
import { 
  Shield, 
  ArrowRight, 
  FileText, 
  Search, 
  Calendar, 
  CheckCircle, 
  PhoneCall, 
  Users, 
  HeartPulse, 
  Clock, 
  Sparkles,
  Building2,
  Stethoscope
} from 'lucide-react';

export default function HomeView({ onNavigate }) {
  const stats = [
    { label: "Specialist Doctors", value: "15+", sub: "Board-Certified", icon: Stethoscope },
    { label: "Patients Served", value: "25,000+", sub: "Exemplary Care", icon: Users },
    { label: "Care Rooms", value: "120+", sub: "Modern ICU & VIP Suites", icon: Building2 },
    { label: "Patient Satisfaction", value: "98.4%", sub: "Audited Quality Score", icon: HeartPulse },
  ];

  const modules = [
    {
      id: "doc_intel",
      title: "Document Intelligence",
      tag: "PyMuPDF & Pydantic",
      desc: "Instant clinical extraction of patient demographics, vital signs, lab panels, medications, and ICD-10 diagnostic codes from PDF summaries.",
      icon: FileText,
      gradient: "from-blue-600 to-indigo-700",
    },
    {
      id: "rag_search",
      title: "Policy RAG Search",
      tag: "Vector Search (ChromaDB)",
      desc: "Semantic retrieval across hospital standard operating procedures, HIPAA protocols, ICU visiting rules, and clinical guidelines with source citations.",
      icon: Search,
      gradient: "from-indigo-600 to-blue-700",
    },
    {
      id: "appointments",
      title: "Smart Appointments",
      tag: "Conversational Booking",
      desc: "Automated multi-turn doctor booking assistant with real-time schedule checks, slot reservation, and persistent MongoDB tracking.",
      icon: Calendar,
      gradient: "from-blue-700 to-sky-700",
    },
    {
      id: "evaluation",
      title: "AI Clinical Evaluation",
      tag: "Ragas Metric Engine",
      desc: "Quantitative evaluation benchmark for medical LLM responses, ensuring strict faithfulness, answer relevancy, and context relevancy.",
      icon: CheckCircle,
      gradient: "from-slate-800 to-blue-900",
    },
  ];

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#0B1340] via-[#101D5E] to-[#1E2FE0] text-white p-8 sm:p-12 md:p-16 shadow-xl shadow-blue-950/15">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -mb-12 -ml-12 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 text-xs font-semibold tracking-wide backdrop-blur-sm">
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>Next-Generation Clinical Administration</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight leading-[1.15]">
            World-Class Care Backed by <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-sky-200">Autonomous AI</span>
          </h1>

          <p className="text-base sm:text-lg text-slate-200 font-normal leading-relaxed max-w-2xl">
            AegisMed empowers hospitals, physicians, and administrative teams with automated clinical record parsing, zero-hallucination policy retrieval, and intelligent patient scheduling.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4">
            <button
              onClick={() => onNavigate('dashboard')}
              className="px-6 py-3.5 rounded-xl bg-white text-blue-900 font-bold text-sm sm:text-base shadow-lg shadow-black/10 hover:bg-blue-50 active:scale-95 transition-all flex items-center gap-2 cursor-pointer"
            >
              <span>Explore Dashboard</span>
              <ArrowRight className="w-4 h-4 stroke-[2.5]" />
            </button>
            <button
              onClick={() => onNavigate('appointments')}
              className="px-6 py-3.5 rounded-xl bg-white/15 border border-white/30 text-white font-semibold text-sm sm:text-base backdrop-blur-sm hover:bg-white/20 active:scale-95 transition-all cursor-pointer"
            >
              Book Consultation 📅
            </button>
          </div>
        </div>
      </section>

      {/* Floating Stats Overview */}
      <section className="-mt-8 sm:-mt-10 max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((s, idx) => {
            const Icon = s.icon;
            return (
              <div 
                key={idx}
                className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-md shadow-blue-500/5 hover:-translate-y-1 transition-all"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                    <Icon className="w-6 h-6 stroke-[2]" />
                  </div>
                  <div>
                    <div className="text-2xl font-extrabold text-slate-900 leading-none">{s.value}</div>
                    <div className="text-sm font-bold text-slate-700 mt-1">{s.label}</div>
                    <div className="text-xs text-slate-400 font-medium">{s.sub}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Core Enterprise Modules */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Integrated Clinical Operations Modules
          </h2>
          <p className="text-sm sm:text-base text-slate-500 font-medium">
            Seamlessly navigate between automated clinical intelligence pipelines with a single click.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {modules.map((m) => {
            const Icon = m.icon;
            return (
              <div
                key={m.id}
                onClick={() => onNavigate(m.id)}
                className="group relative bg-white p-7 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-400/50 hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col justify-between"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${m.gradient} text-white flex items-center justify-center shadow-md shadow-blue-500/20`}>
                      <Icon className="w-6 h-6 stroke-[2.2]" />
                    </div>
                    <span className="text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
                      {m.tag}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                      {m.title}
                    </h3>
                    <p className="text-sm text-slate-500 mt-2 leading-relaxed">
                      {m.desc}
                    </p>
                  </div>
                </div>

                <div className="pt-5 mt-4 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-blue-600 group-hover:translate-x-1 transition-transform">
                  <span>Launch Application</span>
                  <ArrowRight className="w-4 h-4" />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Emergency Assistance Banner */}
      <section className="bg-gradient-to-r from-blue-700 via-indigo-700 to-blue-800 rounded-2xl p-8 sm:p-10 text-white shadow-lg shadow-blue-900/20">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2 text-center md:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 text-xs font-bold uppercase tracking-wider">
              <Clock className="w-3.5 h-3.5" />
              <span>24/7 Rapid Response Protocol</span>
            </div>
            <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Emergency Code Blue & Trauma Support
            </h3>
            <p className="text-sm text-blue-100 max-w-xl">
              Dedicated intensive care triage, critical care ambulances, and on-call specialist surgeons available 24/7 for immediate life support.
            </p>
          </div>

          <div className="flex items-center gap-4 shrink-0 bg-white p-4 sm:p-5 rounded-2xl shadow-lg shadow-black/10 text-slate-900">
            <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <PhoneCall className="w-6 h-6 stroke-[2.4]" />
            </div>
            <div>
              <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Emergency Hotline</div>
              <div className="text-xl font-extrabold text-blue-700 tracking-tight">(021) 1234 5678</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

