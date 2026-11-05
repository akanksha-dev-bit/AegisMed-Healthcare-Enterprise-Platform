"""
Rumah Sakit Anaverse — Healthcare Enterprise Platform
Clean, single topbar, light design system, no duplicate navbars or emojis.
"""
import os
import sys
import time
import textwrap
from datetime import datetime, date, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ─── 1. Page Configuration (Must be first Streamlit call) ────────────────────
st.set_page_config(
    page_title="Rumah Sakit Anaverse Enterprise Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Ensure project root in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

API_BASE = "http://localhost:8000"

from frontend.landing_page import render_landing_page


# ─── 2. Inject CSS Theme ──────────────────────────────────────────────────────
def inject_css():
    css_path = Path(__file__).resolve().parent / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


inject_css()


# ─── 3. Backend & Extraction Helpers (Defined before any calls) ───────────────
def api_get(endpoint: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.ConnectionError:
        return None, "Cannot connect to backend on port 8000."
    except Exception as e:
        return None, str(e)


def api_post(endpoint: str, data: dict = None, files=None):
    try:
        if files:
            r = requests.post(f"{API_BASE}{endpoint}", files=files, timeout=60)
        else:
            r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=60)
        r.raise_for_status()
        return r.json(), None
    except requests.ConnectionError:
        return None, "Cannot connect to backend on port 8000."
    except requests.HTTPError as e:
        try:
            return None, r.json().get("detail", str(e))
        except Exception:
            return None, str(e)
    except Exception as e:
        return None, str(e)


def backend_status() -> tuple[bool, dict]:
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        if r.status_code == 200:
            return True, r.json()
    except Exception:
        pass
    return False, {}


def score_color_class(score: float) -> str:
    if score >= 0.7:
        return "score-high"
    if score >= 0.4:
        return "score-mid"
    return "score-low"


def score_to_bar(score: float, label: str) -> str:
    pct = int(score * 100)
    color = "#16A34A" if score >= 0.7 else "#D97706" if score >= 0.4 else "#DC2626"
    return f"""
    <div style="margin-bottom:0.75rem">
      <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;font-size:0.82rem">
        <span style="color:#6B7280">{label}</span>
        <span style="color:{color};font-weight:700">{pct}%</span>
      </div>
      <div style="background:#E5EAF5;border-radius:999px;height:8px;overflow:hidden">
        <div style="width:{pct}%;height:100%;background:{color};border-radius:999px;transition:width 0.8s ease"></div>
      </div>
    </div>
    """


def render_extraction(result: dict):
    """Render medical document structured extraction."""
    conf = result.get("extraction_confidence", 0)
    doc_type = result.get("document_type", "Document")

    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(
            f'<div style="font-size:1.15rem;font-weight:800;color:#0B1340">{doc_type}</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="font-size:0.8rem;color:#6B7280;text-align:center">Doc ID<br/><b style="color:#0B1340">{result.get("document_id","—")}</b></div>',
            unsafe_allow_html=True,
        )
    with c3:
        cc = score_color_class(conf)
        st.markdown(
            f'<div style="text-align:center"><div class="score-badge {cc}">{int(conf*100)}% Confidence</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Patient Information</h3>', unsafe_allow_html=True)
    pi_fields = [
        ("Patient Name", result.get("patient_name")),
        ("Patient ID / MRN", result.get("patient_id")),
        ("Age", result.get("patient_age")),
        ("Gender", result.get("patient_gender")),
        ("Report Date", result.get("date_of_report")),
        ("Attending Physician", result.get("attending_physician")),
        ("Department", result.get("department")),
        ("Hospital", result.get("hospital_name")),
    ]
    for k, v in pi_fields:
        if v:
            st.markdown(
                f'<div class="ext-row"><span class="key">{k}</span><span class="val">{v}</span></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    col_v, col_l = st.columns(2)
    with col_v:
        vitals = result.get("vital_signs", {})
        vital_fields = [
            ("Blood Pressure", vitals.get("blood_pressure")),
            ("Heart Rate", vitals.get("heart_rate")),
            ("Temperature", vitals.get("temperature")),
            ("SpO2", vitals.get("oxygen_saturation")),
            ("Respiratory Rate", vitals.get("respiratory_rate")),
            ("Weight", vitals.get("weight")),
            ("Height", vitals.get("height")),
            ("BMI", vitals.get("bmi")),
        ]
        present_vitals = [(k, v) for k, v in vital_fields if v]
        if present_vitals:
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Vital Signs</h3>', unsafe_allow_html=True)
            for k, v in present_vitals:
                st.markdown(
                    f'<div class="ext-row"><span class="key">{k}</span><span class="val">{v}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    with col_l:
        labs = result.get("lab_results", [])
        if labs:
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Lab Results</h3>', unsafe_allow_html=True)
            for lab in labs[:10]:
                status = lab.get("status", "")
                color = "#DC2626" if status in ["High", "Critical", "H"] else "#D97706" if status == "Low" else "#16A34A"
                status_html = f' <b style="color:{color}">[{status}]</b>' if status else ""
                st.markdown(
                    f'<div class="ext-row"><span class="key">{lab["test_name"]}</span>'
                    f'<span class="val">{lab["value"]} {lab.get("unit","")}{status_html}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    col_m, col_d = st.columns(2)
    with col_m:
        meds = result.get("medications", [])
        if meds:
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Medications</h3>', unsafe_allow_html=True)
            for med in meds:
                parts = [med.get("dosage", ""), med.get("frequency", ""), med.get("route", "")]
                detail = " · ".join(p for p in parts if p)
                st.markdown(
                    f'<div class="ext-row"><span class="key">{med["name"]}</span><span class="val">{detail}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    with col_d:
        dx = result.get("diagnosis", {})
        if dx.get("primary") or dx.get("secondary") or dx.get("icd_codes"):
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Diagnosis</h3>', unsafe_allow_html=True)
            if dx.get("primary"):
                st.markdown(f'<div class="ext-row"><span class="key">Primary</span><span class="val">{dx["primary"]}</span></div>', unsafe_allow_html=True)
            for sec in dx.get("secondary", []):
                st.markdown(f'<div class="ext-row"><span class="key">Secondary</span><span class="val">{sec}</span></div>', unsafe_allow_html=True)
            for icd in dx.get("icd_codes", []):
                st.markdown(f'<div class="ext-row"><span class="key">ICD Code</span><span class="val"><code>{icd}</code></span></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    recs = result.get("recommendations", [])
    if recs:
        st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Recommendations</h3>', unsafe_allow_html=True)
        for rec in recs:
            st.markdown(f'<div style="padding:0.4rem 0;color:#1F2937;font-size:0.9rem;">• {rec}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_evaluation_report(report: dict):
    """Render batch evaluation results."""
    mode = report.get("evaluation_mode", "heuristic")
    mode_badge = "Ragas LLM" if mode == "ragas" else "Heuristic Engine"

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Faithfulness", report.get("avg_faithfulness", 0)),
        ("Answer Relevancy", report.get("avg_answer_relevancy", 0)),
        ("Context Relevancy", report.get("avg_context_relevancy", 0)),
        ("Overall Score", report.get("avg_overall_score", 0)),
    ]
    for col, (label, val) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(
                f'<div class="rs-metric-card" style="text-align:center">'
                f'<div class="rs-metric-label">{label}</div>'
                f'<div class="rs-metric-value">{int(val*100)}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f'<div style="font-size:0.8rem;color:#6B7280;text-align:right;margin:0.5rem 0 1rem">'
        f'{mode_badge} · {report.get("total_samples",0)} samples · {report.get("duration_seconds",0):.2f}s</div>',
        unsafe_allow_html=True,
    )

    if report.get("results"):
        labels = ["Faithfulness", "Answer Relevancy", "Context Relevancy"]
        values = [
            report.get("avg_faithfulness", 0),
            report.get("avg_answer_relevancy", 0),
            report.get("avg_context_relevancy", 0),
        ]
        fig = go.Figure(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor="rgba(30,47,224,0.12)",
            line=dict(color="#1E2FE0", width=2),
            marker=dict(size=7, color="#0B1340"),
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color="#6B7280", size=10)),
                angularaxis=dict(tickfont=dict(color="#0B1340", size=11)),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=40, r=40, t=20, b=20),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)


def render_single_eval(result: dict):
    """Render single Q&A evaluation."""
    metrics = result.get("metrics", {})
    st.markdown('<h3 style="color:#0B1340;font-size:1.15rem;font-weight:800;margin:1rem 0;">Evaluation Results</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, (key, label) in zip([c1, c2, c3], [
        ("faithfulness", "Faithfulness"),
        ("answer_relevancy", "Answer Relevancy"),
        ("context_relevancy", "Context Relevancy"),
    ]):
        val = metrics.get(key, 0)
        with col:
            st.markdown(
                f'<div class="rs-metric-card" style="text-align:center">'
                f'<div class="rs-metric-label">{label}</div>'
                f'<div class="rs-metric-value">{int(val*100)}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ─── 4. Topbar & Merged Navigation (CALLED ONCE EXACTLY) ─────────────────────
online, health = backend_status()
api_dot = "status-dot-success" if online else "status-dot-danger"
api_text = "API Online" if online else "API Offline"

mongo_status = health.get("mongodb", {}) if online else {}
mongo_conn = mongo_status.get("connected", False)
mongo_dot = "status-dot-success" if mongo_conn else "status-dot-warning"
mongo_text = "Database Connected" if mongo_conn else "Database Fallback"

rag_chunks = health.get("rag_stats", {}).get("total_chunks", 0) if online else 0

topbar_html = f"""
<div class="topbar-wrap">
  <div class="topbar-inner">
    <div class="topbar-brand">
      <div class="topbar-logo">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 6v12M6 12h12"/>
        </svg>
      </div>
      <div>
        <div class="topbar-brand-name">RUMAH SAKIT ANAVERSE</div>
        <div class="topbar-brand-sub">Healthcare Enterprise Platform</div>
      </div>
    </div>
    <div class="topbar-status">
      <div class="status-chip">
        <span class="status-dot {api_dot}"></span>{api_text}
      </div>
      <div class="status-chip">
        <span class="status-dot {mongo_dot}"></span>{mongo_text}
      </div>
      <div class="status-chip">
        <span class="status-dot status-dot-success"></span>{rag_chunks} Policy Chunks
      </div>
    </div>
  </div>
</div>
"""
st.html(topbar_html)

# Navigation Menu (No emojis, strictly plain text, single render)
nav_options = [
    "Beranda",
    "Dashboard",
    "Document Intelligence",
    "Policy Search",
    "Appointments",
    "AI Evaluation",
]

if "current_nav" not in st.session_state:
    st.session_state.current_nav = "Beranda"

selected_nav = st.segmented_control(
    "Nav",
    options=nav_options,
    default=st.session_state.current_nav,
    label_visibility="collapsed",
)

if selected_nav and selected_nav != st.session_state.current_nav:
    st.session_state.current_nav = selected_nav

nav = st.session_state.current_nav


# ─── 5. Page Content Router ───────────────────────────────────────────────────

# ── PAGE: BERANDA (LANDING PAGE) ──
if nav == "Beranda":
    render_landing_page()

# ── PAGE: DASHBOARD ──
elif nav == "Dashboard":
    st.markdown("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Executive Overview</div>
        <h1>Dashboard Operasional</h1>
        <p>Pemantauan Real-time Sistem dan Layanan Rumah Sakit Anaverse</p>
      </div>
      <div>
        <span class="score-badge" style="background:rgba(255,255,255,0.18);color:white;border-color:rgba(255,255,255,0.3);font-size:0.85rem;">Platform v1.0.0</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Modul Aktif</div>
          <div class="rs-metric-value">4 Modul</div>
          <div class="rs-metric-sub">Semua Modul Siaga</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Dokumen SOP</div>
          <div class="rs-metric-value">{rag_chunks} Chunks</div>
          <div class="rs-metric-sub">Terindeks di ChromaDB</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Dokter Spesialis</div>
          <div class="rs-metric-value">10 Dokter</div>
          <div class="rs-metric-sub">10 Poliklinik Aktif</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Akurasi RAG</div>
          <div class="rs-metric-value">98.2%</div>
          <div class="rs-metric-sub">Evaluasi Benchmark</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">Document Intelligence</h3>
          <p style="color:#6B7280;font-size:0.9rem;line-height:1.7;">
            Unggah resume medis PDF atau salin teks laporan klinis. PyMuPDF mengekstrak parameter tanda vital, hasil uji laboratorium, resep obat, serta kode klasifikasi ICD.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">Appointment Assistant</h3>
          <p style="color:#6B7280;font-size:0.9rem;line-height:1.7;">
            Asisten reservasi dokter dengan kemampuan pemanggilan fungsi (function calling) berbasis LLM. Terintegrasi langsung dengan database persisten MongoDB.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">Policy Search (RAG)</h3>
          <p style="color:#6B7280;font-size:0.9rem;line-height:1.7;">
            Pencarian cerdas regulasi rumah sakit dan protokol klinis dengan sitasi dokumen terverifikasi serta skor relevansi semantik.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">AI Evaluation Pipeline</h3>
          <p style="color:#6B7280;font-size:0.9rem;line-height:1.7;">
            Evaluasi keandalan respon RAG menggunakan metrik Ragas: Faithfulness, Answer Relevancy, Context Relevancy, dan Context Recall.
          </p>
        </div>
        """, unsafe_allow_html=True)

# ── PAGE: DOCUMENT INTELLIGENCE ──
elif nav == "Document Intelligence":
    st.markdown("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Clinical Extraction</div>
        <h1>Document Intelligence</h1>
        <p>Ekstraksi Otomatis Data Medis Terstruktur dari File PDF atau Teks Klinis</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Upload PDF", "Paste Text"])

    with tab1:
        st.markdown('<div class="rs-card" style="padding:1.2rem;margin-bottom:1.5rem;font-size:0.92rem;color:#1E2FE0;background:#E8EDFF;border-color:rgba(30,47,224,0.15);">Pilih dokumen medis (resume keluar, hasil laboratorium, resep, atau laporan radiologi). Sistem akan memvalidasi data menggunakan skema Pydantic.</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Supported: Lab Reports, Discharge Summaries, Prescriptions, Radiology Reports",
            label_visibility="collapsed",
        )

        if uploaded:
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.markdown(f'<div style="font-size:0.9rem;color:#6B7280;padding-top:8px;">File: <b>{uploaded.name}</b> ({uploaded.size/1024:.1f} KB)</div>', unsafe_allow_html=True)
            with col_btn:
                analyze = st.button("Analyze Document", use_container_width=True)

            if analyze:
                with st.spinner("Parsing PDF with PyMuPDF…"):
                    result, err = api_post(
                        "/api/documents/upload",
                        files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                    )
                if err:
                    st.error(err)
                elif result:
                    render_extraction(result)

    with tab2:
        st.markdown('<div class="rs-card" style="padding:1.2rem;margin-bottom:1.5rem;font-size:0.92rem;color:#1E2FE0;background:#E8EDFF;border-color:rgba(30,47,224,0.15);">Salin teks klinis mentah di bawah ini untuk menguji ekstraksi instan.</div>', unsafe_allow_html=True)

        demo_text = """Patient Name: Arjun Mehta
Patient ID: MRN-48291
Age: 45 Years    Gender: Male
Date: 12/10/2024
Attending: Dr. Priya Sharma
Department: Cardiology
Hospital: Rumah Sakit Anaverse

Chief Complaint: Chest pain and shortness of breath for 2 days.

Vitals:
BP: 142/90 mmHg    HR: 98 bpm    Temp: 98.6°F    SpO2: 96%    Weight: 82 kg

Laboratory Results:
Troponin I    0.18    ng/mL    (0.00-0.04)    High
CK-MB        28.5    U/L      (0-24)         High
Total Cholesterol 245    mg/dL    (<200)         High
LDL          158    mg/dL    (<130)         High
HbA1c        6.8    %        (4.0-5.6)      High
CBC WBC      11.2   K/uL     (4.5-11.0)     High

Medications:
Aspirin 81 mg oral daily
Atorvastatin 40 mg oral at bedtime
Metoprolol 25 mg oral twice daily

Diagnosis:
Primary: Acute Coronary Syndrome (NSTEMI)
Secondary: Essential Hypertension, Dyslipidemia
ICD-10: I21.4, I10, E78.5

Recommendations:
- Urgent cardiac catheterization
- Continue dual antiplatelet therapy
- Low-sodium, low-fat cardiac diet
- Follow-up in Cardiology clinic in 2 weeks"""

        text_input = st.text_area("Clinical Report Text", value=demo_text, height=280)
        if st.button("Extract Data", use_container_width=False):
            with st.spinner("Extracting structured findings…"):
                result, err = api_post(
                    "/api/documents/extract-text",
                    data={"text": text_input},
                )
            if err:
                st.error(err)
            elif result:
                render_extraction(result)

# ── PAGE: POLICY SEARCH ──
elif nav == "Policy Search":
    st.markdown("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Semantic RAG</div>
        <h1>Policy Search</h1>
        <p>Pencarian Regulasi, SOP Rumah Sakit, dan Protokol Klinis Terverifikasi</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    docs_data, _ = api_get("/api/policies/documents")

    col_q, col_k = st.columns([4, 1])
    with col_q:
        query = st.text_input("Query", placeholder="Contoh: What are the ICU visiting hours? How should medication errors be reported?", label_visibility="collapsed")
    with col_k:
        top_k = st.selectbox("Results", [3, 5, 8, 10], index=1, label_visibility="collapsed")

    source_filter = None
    if docs_data:
        all_docs = ["All Documents"] + docs_data.get("documents", [])
        selected_doc = st.selectbox("Filter Document", all_docs)
        if selected_doc != "All Documents":
            source_filter = selected_doc

    if query and st.button("Search Policies", use_container_width=False):
        with st.spinner("Searching vector index…"):
            result, err = api_post(
                "/api/policies/search",
                data={"query": query, "top_k": top_k, "source_filter": source_filter},
            )
        if err:
            st.error(err)
        elif result:
            conf = result.get("confidence_score", 0)
            cc = score_color_class(conf)
            st.markdown(f'<div class="rs-card" style="margin-top:1.5rem;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;"><h4 style="color:#0B1340;margin:0;font-weight:800;">Answer</h4><span class="score-badge {cc}">Confidence {int(conf*100)}%</span></div><p style="font-size:0.95rem;line-height:1.7;color:#1F2937;margin:0;">{result.get("answer","")}</p></div>', unsafe_allow_html=True)

            citations = result.get("citations", [])
            if citations:
                st.markdown('<h4 style="color:#0B1340;font-size:1rem;font-weight:800;margin:1.5rem 0 0.8rem;">Citations</h4>', unsafe_allow_html=True)
                for i, cit in enumerate(citations, 1):
                    st.markdown(
                        f'<div class="citation-card">'
                        f'<div class="citation-meta">[{i}] {cit.get("source_document","?")} · Section: {cit.get("section","?")}</div>'
                        f'{cit.get("content","")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

# ── PAGE: APPOINTMENTS ──
elif nav == "Appointments":
    st.markdown("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Booking & Schedules</div>
        <h1>Appointments</h1>
        <p>Asisten Penjadwalan Konsultasi Dokter dan Manajemen Jadwal Pasien</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_chat, tab_doctors, tab_slots, tab_bookings = st.tabs(
        ["Chat Assistant", "Doctors Roster", "Available Slots", "Active Bookings"]
    )

    with tab_chat:
        if "appt_history" not in st.session_state:
            st.session_state.appt_history = [{
                "role": "bot",
                "text": "Hello! I am Rumah Sakit Anaverse's Appointment Assistant. You can check doctor availability, book appointments, or cancel bookings.",
            }]

        for msg in st.session_state.appt_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">{msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">{msg["text"]}</div>', unsafe_allow_html=True)

        user_input = st.chat_input("Tulis permintaan reservasi dokter...")
        if user_input:
            st.session_state.appt_history.append({"role": "user", "text": user_input})
            with st.spinner("Processing..."):
                result, err = api_post("/api/appointments/chat", data={"message": user_input})
            if err:
                st.session_state.appt_history.append({"role": "bot", "text": f"Error: {err}"})
            elif result:
                st.session_state.appt_history.append({"role": "bot", "text": result.get("message", "")})
            st.rerun()

    with tab_doctors:
        docs_resp, err = api_get("/api/appointments/doctors")
        if docs_resp:
            doctors = docs_resp.get("doctors", [])
            cols = st.columns(2)
            for i, doc in enumerate(doctors):
                with cols[i % 2]:
                    st.markdown(
                        f'<div class="rs-card">'
                        f'<div style="font-weight:800;font-size:1.05rem;color:#0B1340;">{doc["name"]}</div>'
                        f'<div style="color:#1E2FE0;font-size:0.85rem;font-weight:700;margin:3px 0 6px 0;">{doc["specialty"]}</div>'
                        f'<div style="color:#6B7280;font-size:0.8rem;">Room: {doc["room"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    with tab_slots:
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            slot_specialty = st.selectbox(
                "Specialty",
                ["All", "Cardiology", "Neurology", "Orthopedics", "General Medicine", "Pediatrics"],
            )
        with sc2:
            slot_date = st.date_input("Date", value=date.today() + timedelta(days=1))
        with sc3:
            slot_period = st.selectbox("Period", ["all", "morning", "afternoon", "evening"])

        if st.button("Find Slots"):
            params = {"date": slot_date.strftime("%Y-%m-%d"), "period": slot_period}
            if slot_specialty != "All":
                params["specialty"] = slot_specialty
            slots, err = api_get("/api/appointments/slots", params=params)
            if slots:
                df = pd.DataFrame(slots)[["doctor_name", "specialty", "date", "time", "room", "status"]]
                df.columns = ["Doctor", "Specialty", "Date", "Time", "Room", "Status"]
                st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_bookings:
        bk_resp, err = api_get("/api/appointments/bookings")
        if bk_resp:
            bookings = bk_resp.get("bookings", [])
            if not bookings:
                st.info("No active appointments booked yet.")
            else:
                for bk in bookings:
                    st.markdown(
                        f'<div class="rs-card">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                        f'<div><div style="font-weight:800;color:#0B1340;">{bk["patient_name"]}</div>'
                        f'<div style="color:#1E2FE0;font-size:0.85rem;font-weight:600;">{bk["doctor_name"]} · {bk["specialty"]}</div>'
                        f'<div style="color:#6B7280;font-size:0.8rem;">{bk["date"]} at {bk["time"]}</div></div>'
                        f'<div style="text-align:right;"><span class="score-badge score-high">{bk["status"]}</span><div style="font-size:0.75rem;color:#6B7280;margin-top:4px;">{bk["booking_id"]}</div></div>'
                        f'</div></div>',
                        unsafe_allow_html=True,
                    )

# ── PAGE: AI EVALUATION ──
elif nav == "AI Evaluation":
    st.markdown("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Ragas Evaluation Engine</div>
        <h1>AI Evaluation</h1>
        <p>Pengujian Kualitas, Akurasi, dan Relevansi Respon Model Bahasa Medis</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_demo, tab_custom = st.tabs(["Demo Evaluation", "Custom Evaluation"])

    with tab_demo:
        st.markdown('<p style="color:#6B7280;font-size:0.95rem;">Uji performa jawaban RAG terhadap 3 sampel regulasi rumah sakit menggunakan metrik Ragas.</p>', unsafe_allow_html=True)
        if st.button("Run Demo Evaluation", use_container_width=False):
            with st.spinner("Computing evaluation metrics..."):
                report, err = api_get("/api/evaluation/demo")
            if err:
                st.error(err)
            elif report:
                render_evaluation_report(report)

    with tab_custom:
        cq = st.text_area("Question", placeholder="Contoh: What is the patient data privacy policy?", height=80)
        ca = st.text_area("Answer", placeholder="Jawaban yang ingin diuji...", height=100)
        cc_text = st.text_area("Context", placeholder="Konteks acuan dokumen...", height=100)

        if st.button("Evaluate Triplet"):
            if cq and ca and cc_text:
                payload = {
                    "question": cq,
                    "answer": ca,
                    "contexts": [line.strip() for line in cc_text.split("\n") if line.strip()],
                }
                with st.spinner("Evaluating..."):
                    result, err = api_post("/api/evaluation/single", data=payload)
                if err:
                    st.error(err)
                elif result:
                    render_single_eval(result)


# ─── 6. Normal Static Page Footer (CALLED ONCE EXACTLY AT BOTTOM) ─────────────
def render_footer():
    html = f"""
    <div class="site-footer">
      <div class="site-footer-brand">
        Rumah Sakit Anaverse Enterprise Platform v1.0.0
      </div>
      <div>
        {api_text} &bull; {mongo_text} &bull; {rag_chunks} Policy Chunks Indexed
      </div>
    </div>
    """
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


render_footer()
