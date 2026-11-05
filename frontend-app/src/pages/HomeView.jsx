import React from 'react';
import { 
  Shield, 
  ArrowRight, 
  Calendar, 
  Clock, 
  Award, 
  Building2, 
  Stethoscope, 
  Activity, 
  PhoneCall, 
  CheckCircle2, 
  Star,
  Heart,
  ChevronRight
} from 'lucide-react';

export default function HomeView({ onNavigate }) {
  const stats = [
    { value: "15+", label: "Specialist Doctors", desc: "Board-Certified Leaders" },
    { value: "25,000+", label: "Patients Served", desc: "High Quality Clinical Care" },
    { value: "120+", label: "Inpatient Rooms", desc: "ICU, High Care & VIP Suites" },
    { value: "98%", label: "Patient Satisfaction", desc: "Independent Audit Score" },
  ];

  const services = [
    { title: "Specialist Clinics", img: "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=400&q=80" },
    { title: "Inpatient Care", img: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80" },
    { title: "24/7 Emergency (ER)", img: "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80" },
    { title: "Advanced Radiology", img: "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=400&q=80" },
    { title: "Diagnostic Lab", img: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=400&q=80" },
    { title: "24/7 Pharmacy", img: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=400&q=80" },
  ];

  const doctors = [
    {
      name: "Dr. Andika Pratama, Sp.JP",
      spec: "Cardiologist & Vascular Specialist",
      rating: "4.9",
      img: "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=500&q=80",
    },
    {
      name: "Dr. Salsabila Putri, Sp.A",
      spec: "Pediatric Specialist",
      rating: "4.9",
      img: "https://images.unsplash.com/photo-1594824813511-30c1154564c7?auto=format&fit=crop&w=500&q=80",
    },
    {
      name: "Dr. Budi Santoso, Sp.B",
      spec: "General & Laparoscopic Surgeon",
      rating: "4.8",
      img: "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&w=500&q=80",
    },
    {
      name: "Dr. Meilani Putri, Sp.PD",
      spec: "Internal Medicine Specialist",
      rating: "4.9",
      img: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=500&q=80",
    },
  ];

  const facilities = [
    { title: "Intensive Care Unit (ICU)", img: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=300&q=80" },
    { title: "VIP Inpatient Suite", img: "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=300&q=80" },
    { title: "Modern Operating Theater", img: "https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=300&q=80" },
    { title: "Clinical Laboratory", img: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=300&q=80" },
    { title: "24/7 Mobile Ambulance", img: "https://images.unsplash.com/photo-1587745416684-47953f16f02f?auto=format&fit=crop&w=300&q=80" },
  ];

  const articles = [
    {
      tag: "Cardiovascular Health",
      tagColor: "bg-red-50 text-red-600 border-red-200",
      title: "5 Evidence-Based Dietary Habits to Prevent Coronary Artery Disease",
      date: "03 November 2026 · 4 min read",
      img: "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=500&q=80",
    },
    {
      tag: "Pediatric Care",
      tagColor: "bg-amber-50 text-amber-600 border-amber-200",
      title: "Essential Immunization Schedules for Optimal Childhood Development",
      date: "01 November 2026 · 3 min read",
      img: "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=500&q=80",
    },
    {
      tag: "Preventive Lifestyle",
      tagColor: "bg-emerald-50 text-emerald-600 border-emerald-200",
      title: "Balancing Mental and Physical Resilience in Modern Healthcare Environments",
      date: "28 October 2026 · 5 min read",
      img: "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=500&q=80",
    },
    {
      tag: "Geriatric Wellness",
      tagColor: "bg-indigo-50 text-indigo-600 border-indigo-200",
      title: "Preserving Bone Density and Joint Mobility in the Golden Years",
      date: "25 October 2026 · 4 min read",
      img: "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=500&q=80",
    },
  ];

  return (
    <div className="space-y-20 pb-16">
      
      {/* ── 1. HERO SECTION (Doctor with young girl patient image + straight accreditation badge) ── */}
      <section className="pt-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Left Text */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-bold tracking-wide shadow-xs">
              <Heart className="w-4 h-4 fill-blue-600 text-blue-600" />
              <span>Your Health is Our Top Priority</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-[#0B1340] tracking-tight leading-[1.15]">
              World-Class Care for Your <span className="text-blue-600">Health</span> and Family
            </h1>

            <p className="text-base sm:text-lg text-slate-500 font-medium leading-relaxed max-w-xl">
              We provide premier healthcare delivery combining experienced clinical specialists, state-of-the-art diagnostic facilities, and compassionate patient care.
            </p>

            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={() => onNavigate('dashboard')}
                className="px-6 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 active:scale-95 text-white font-bold text-sm sm:text-base shadow-lg shadow-blue-600/30 flex items-center gap-2 transition-all cursor-pointer"
              >
                <span>View Clinical Services</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={() => onNavigate('appointments')}
                className="px-6 py-3.5 rounded-xl bg-white hover:bg-slate-50 active:scale-95 text-blue-700 font-bold text-sm sm:text-base border border-slate-200 shadow-xs flex items-center gap-2 transition-all cursor-pointer"
              >
                <Calendar className="w-4 h-4 text-blue-600" />
                <span>Book Appointment</span>
              </button>
            </div>
          </div>

          {/* Right Doctor Image */}
          <div className="relative flex justify-center">
            <div className="w-full max-w-[500px] h-[460px] rounded-3xl overflow-hidden shadow-2xl shadow-blue-900/10 border-8 border-white relative bg-blue-50">
              <img 
                src="/assets/hero.jpg" 
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=900&q=80";
                }}
                alt="Doctor with Young Girl Patient" 
                className="w-full h-full object-cover object-top"
              />

              {/* Straight Floating Accreditation Badge */}
              <div className="absolute bottom-5 left-5 bg-white/95 backdrop-blur-md p-3.5 px-4 rounded-2xl border border-white/80 shadow-lg shadow-blue-900/10 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                  <Shield className="w-5 h-5 fill-blue-600/20 stroke-[2.2]" />
                </div>
                <div>
                  <div className="text-xs font-black text-slate-900">National Healthcare Accreditation</div>
                  <div className="text-[10px] font-semibold text-slate-500">Ministry of Health Certified Standard</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>


      {/* ── 2. FLOATING STATS CARD ── */}
      <section className="bg-white rounded-3xl border border-slate-200/90 p-8 shadow-lg shadow-blue-500/5">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((s, idx) => (
            <div key={idx} className="flex items-center gap-4">
              <div className="w-13 h-13 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                <Activity className="w-6 h-6 stroke-[2]" />
              </div>
              <div>
                <div className="text-3xl font-extrabold text-[#0B1340]">{s.value}</div>
                <div className="text-sm font-bold text-slate-800">{s.label}</div>
                <div className="text-xs text-slate-400 font-medium">{s.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </section>


      {/* ── 3. ABOUT HOSPITAL SECTION ── */}
      <section className="pt-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Hospital Building Image */}
          <div className="rounded-3xl overflow-hidden h-[420px] shadow-xl shadow-slate-900/5 border border-slate-200">
            <img 
              src="https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?auto=format&fit=crop&w=900&q=80" 
              alt="AegisMed Hospital Building" 
              className="w-full h-full object-cover"
            />
          </div>

          {/* About Description & 4 Pillars */}
          <div className="space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-700 text-xs font-bold border border-blue-200">
              About AegisMed
            </div>

            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#0B1340] tracking-tight">
              AegisMed Hospital for a <span className="text-blue-600">Healthier</span> Tomorrow
            </h2>

            <p className="text-slate-500 text-sm sm:text-base leading-relaxed">
              Founded on the pillars of clinical safety and human-centered innovation, we unite specialized physicians with cutting-edge medical technology to deliver comprehensive, compassionate, and trustworthy healthcare.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-2">
              {[
                { title: "24/7 Medical Service", sub: "Round-the-clock emergency care", icon: Clock },
                { title: "Board-Certified Staff", sub: "Top clinical specialists", icon: Stethoscope },
                { title: "Modern Facilities", sub: "Advanced medical technology", icon: Building2 },
                { title: "Quality Accreditations", sub: "Strict safety protocols", icon: Award },
              ].map((pill, i) => {
                const Icon = pill.icon;
                return (
                  <div key={i} className="p-3.5 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                      <Icon className="w-5 h-5 stroke-[2]" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-900">{pill.title}</div>
                      <div className="text-[11px] text-slate-400">{pill.sub}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </div>
      </section>


      {/* ── 4. COMPREHENSIVE MEDICAL SERVICES (6 Cards with Pictures) ── */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-700 text-xs font-bold border border-blue-200">
              Clinical Services
            </div>
            <h2 className="text-3xl font-extrabold text-[#0B1340] tracking-tight mt-2">
              Comprehensive Medical <span className="text-blue-600">Specialties</span>
            </h2>
          </div>
          <button 
            onClick={() => onNavigate('dashboard')}
            className="text-sm font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
          >
            <span>Explore All Services</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm">
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {services.map((srv, idx) => (
              <div 
                key={idx} 
                className="bg-slate-50/70 p-2.5 rounded-2xl border border-slate-200/70 hover:border-blue-400 text-center transition-all hover:-translate-y-1 group"
              >
                <div className="w-full h-28 rounded-xl overflow-hidden mb-3 bg-slate-200">
                  <img 
                    src={srv.img} 
                    alt={srv.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <div className="text-xs font-bold text-slate-900 group-hover:text-blue-600 transition-colors pb-1">
                  {srv.title}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>


      {/* ── 5. EXPERIENCED SPECIALIST DOCTORS (With Photos & Star Ratings) ── */}
      <section className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-center">
          
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-700 text-xs font-bold border border-blue-200">
              Doctors Roster
            </div>
            <h2 className="text-3xl font-extrabold text-[#0B1340] tracking-tight leading-tight">
              Experienced Specialist <span className="text-blue-600">Physicians</span>
            </h2>
            <p className="text-slate-500 text-sm leading-relaxed">
              Attended by reputable specialist physicians dedicated to evidence-based diagnostic clarity and patient recovery.
            </p>
            <button
              onClick={() => onNavigate('appointments')}
              className="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-500/20 flex items-center gap-2 cursor-pointer transition-all"
            >
              <span>View All Doctors</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="lg:col-span-3 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            {doctors.map((doc, idx) => (
              <div key={idx} className="bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                <div className="w-full h-48 overflow-hidden relative bg-blue-50">
                  <img 
                    src={doc.img} 
                    alt={doc.name} 
                    className="w-full h-full object-cover object-top"
                  />
                  <div className="absolute top-2.5 right-2.5 bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-full text-xs font-black text-slate-800 shadow-xs flex items-center gap-1">
                    <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    <span>{doc.rating}</span>
                  </div>
                </div>
                <div className="p-4 space-y-1">
                  <h4 className="font-extrabold text-slate-900 text-sm leading-snug">{doc.name}</h4>
                  <p className="text-xs font-semibold text-blue-600">{doc.spec}</p>
                </div>
              </div>
            ))}
          </div>

        </div>
      </section>


      {/* ── 6. MODERN HOSPITAL FACILITIES (Dark Section with Glass Image Tiles) ── */}
      <section className="rounded-3xl bg-gradient-to-br from-[#0B1340] via-[#0E1A54] to-[#16277D] p-8 sm:p-12 text-white shadow-xl">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-center">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 text-white text-xs font-bold border border-white/20">
              Modern Facilities
            </div>
            <h2 className="text-3xl font-extrabold text-white tracking-tight leading-tight">
              State-of-the-Art Care Infrastructure
            </h2>
            <p className="text-slate-300 text-xs sm:text-sm leading-relaxed">
              Designed specifically to meet strict sterility standards and provide a comfortable, restful environment for patients and families.
            </p>
          </div>

          <div className="lg:col-span-3 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
            {facilities.map((fac, idx) => (
              <div key={idx} className="bg-white/10 border border-white/20 rounded-2xl overflow-hidden text-center hover:bg-white/15 transition-all">
                <div className="w-full h-24 overflow-hidden">
                  <img 
                    src={fac.img} 
                    alt={fac.title} 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-2.5 text-xs font-bold text-white">
                  {fac.title}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>


      {/* ── 7. HEALTH ARTICLES & NEWS ── */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-700 text-xs font-bold border border-blue-200">
              Latest Articles
            </div>
            <h2 className="text-3xl font-extrabold text-[#0B1340] tracking-tight mt-2">
              Clinical Insights & Health <span className="text-blue-600">Guidance</span>
            </h2>
          </div>
          <button 
            onClick={() => onNavigate('rag_search')}
            className="text-sm font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
          >
            <span>View All SOPs & Articles</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {articles.map((art, idx) => (
            <div key={idx} className="bg-white rounded-2xl border border-slate-200/90 overflow-hidden shadow-xs hover:shadow-md transition-shadow flex flex-col">
              <div className="w-full h-36 overflow-hidden bg-slate-100">
                <img 
                  src={art.img} 
                  alt={art.title} 
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-5 flex-1 flex flex-col justify-between space-y-3">
                <div className="space-y-2">
                  <span className={`inline-block px-2.5 py-1 rounded-full text-[10px] font-bold border ${art.tagColor}`}>
                    {art.tag}
                  </span>
                  <h4 className="font-extrabold text-slate-900 text-sm leading-snug">
                    {art.title}
                  </h4>
                </div>
                <div className="text-[11px] font-semibold text-slate-400">
                  {art.date}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>


      {/* ── 8. EMERGENCY CTA BANNER & HOTLINE ── */}
      <section className="bg-gradient-to-r from-blue-700 via-indigo-700 to-blue-800 rounded-3xl p-8 sm:p-12 text-white shadow-xl shadow-blue-900/20">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              Need Immediate Medical Assistance?
            </h2>
            <p className="text-blue-100 text-sm sm:text-base leading-relaxed max-w-xl">
              Our Emergency Department operates 24 hours a day, 7 days a week. Rapid emergency dispatch with on-site triage nurses and board-certified ER physicians.
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="bg-white/20 px-3.5 py-1.5 rounded-full text-xs font-bold">24/7 Trauma Unit</span>
              <span className="bg-white/20 px-3.5 py-1.5 rounded-full text-xs font-bold">Specialist On-Call</span>
              <span className="bg-white/20 px-3.5 py-1.5 rounded-full text-xs font-bold">Mobile ICU Fleet</span>
            </div>
          </div>

          <div className="bg-white p-7 rounded-2xl text-slate-900 shadow-xl space-y-3 text-center">
            <div className="text-xs font-extrabold uppercase tracking-wider text-slate-400">
              Emergency Hotline
            </div>
            <div className="text-2xl font-black text-blue-700 flex items-center justify-center gap-2">
              <PhoneCall className="w-5 h-5" />
              <span>(021) 1234 5678</span>
            </div>
            <p className="text-xs text-slate-500">Or Schedule an In-Person Consultation</p>
            <button
              onClick={() => onNavigate('appointments')}
              className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-500/20 active:scale-95 transition-all cursor-pointer"
            >
              Book Doctor Consultation
            </button>
          </div>
        </div>
      </section>

    </div>
  );
}
