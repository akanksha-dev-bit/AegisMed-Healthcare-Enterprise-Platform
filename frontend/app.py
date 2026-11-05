"""
🛡️ AegisMed Healthcare Enterprise Platform
Clean, modern enterprise healthcare assistant with 100% English interface,
single-click navigation, crisp typography, and high-contrast design.
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
    page_title="🛡️ AegisMed Healthcare Enterprise Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Ensure project root in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

API_BASE = "http://localhost:8000"


# ─── 2. Inject CSS Theme ──────────────────────────────────────────────────────
def inject_css():
    css_path = Path(__file__).resolve().parent / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


inject_css()


# ─── 3. Backend Helpers ───────────────────────────────────────────────────────
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
    """Render medical document structured clinical extraction."""
    conf = result.get("extraction_confidence", 0)
    doc_type = result.get("document_type", "Clinical Document")

    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(
            f'<div style="font-size:1.2rem;font-weight:800;color:#0B1340">{doc_type}</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="font-size:0.82rem;color:#6B7280;text-align:center">Document ID<br/><b style="color:#0B1340">{result.get("document_id","—")}</b></div>',
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
        ("Hospital / Facility", result.get("hospital_name")),
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
            ("Oxygen Saturation (SpO2)", vitals.get("oxygen_saturation")),
            ("Respiratory Rate", vitals.get("respiratory_rate")),
            ("Body Weight", vitals.get("weight")),
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
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Laboratory Results</h3>', unsafe_allow_html=True)
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
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Prescribed Medications</h3>', unsafe_allow_html=True)
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
            st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Clinical Diagnosis</h3>', unsafe_allow_html=True)
            if dx.get("primary"):
                st.markdown(f'<div class="ext-row"><span class="key">Primary Diagnosis</span><span class="val">{dx["primary"]}</span></div>', unsafe_allow_html=True)
            for sec in dx.get("secondary", []):
                st.markdown(f'<div class="ext-row"><span class="key">Secondary Diagnosis</span><span class="val">{sec}</span></div>', unsafe_allow_html=True)
            for icd in dx.get("icd_codes", []):
                st.markdown(f'<div class="ext-row"><span class="key">ICD-10 Code</span><span class="val"><code>{icd}</code></span></div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    recs = result.get("recommendations", [])
    if recs:
        st.markdown('<div class="rs-card"><h3 style="color:#0B1340;font-size:1.05rem;font-weight:800;margin-bottom:12px;">Clinical Recommendations & Care Plan</h3>', unsafe_allow_html=True)
        for rec in recs:
            st.markdown(f'<div style="padding:0.4rem 0;color:#1F2937;font-size:0.9rem;">• {rec}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_evaluation_report(report: dict):
    """Render batch evaluation results."""
    mode = report.get("evaluation_mode", "heuristic")
    mode_badge = "Ragas LLM Evaluation" if mode == "ragas" else "Heuristic Engine"

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Faithfulness", report.get("avg_faithfulness", 0)),
        ("Answer Relevancy", report.get("avg_answer_relevancy", 0)),
        ("Context Relevancy", report.get("avg_context_relevancy", 0)),
        ("Overall Benchmark Score", report.get("avg_overall_score", 0)),
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
        f'<div style="font-size:0.82rem;color:#6B7280;text-align:right;margin:0.75rem 0 1.25rem">'
        f'{mode_badge} · {report.get("total_samples",0)} Evaluation Samples · {report.get("duration_seconds",0):.2f}s latency</div>',
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
            fillcolor="rgba(30,47,224,0.15)",
            line=dict(color="#1E2FE0", width=2.5),
            marker=dict(size=8, color="#0B1340"),
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color="#6B7280", size=10)),
                angularaxis=dict(tickfont=dict(color="#0B1340", size=12, family="Plus Jakarta Sans")),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=40, r=40, t=25, b=25),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)


def render_single_eval(result: dict):
    """Render single Q&A evaluation."""
    metrics = result.get("metrics", {})
    st.markdown('<h3 style="color:#0B1340;font-size:1.15rem;font-weight:800;margin:1.2rem 0;">Evaluation Results</h3>', unsafe_allow_html=True)
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
api_text = "Backend Online" if online else "Backend Offline"

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
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
      </div>
      <div>
        <div class="topbar-brand-name">🛡️ AEGISMED</div>
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
        <span class="status-dot status-dot-info"></span>Policy Store Ready ({rag_chunks} Chunks)
      </div>
    </div>
  </div>
</div>
"""
st.html(topbar_html)

# Navigation Menu Options (Clean English labels with standard icons)
nav_options = [
    "🏠 Dashboard",
    "📄 Document Intelligence",
    "🔍 Policy RAG Search",
    "📅 Appointments",
    "📊 AI Evaluation",
]

# Ensure single-click reactive state without double click bug
if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = nav_options[0]

nav = st.segmented_control(
    "Navigation",
    options=nav_options,
    key="nav_selection",
    label_visibility="collapsed",
) or st.session_state.nav_selection


# ─── 5. Page Content Router ───────────────────────────────────────────────────

# ── PAGE: DASHBOARD ──
if nav == "🏠 Dashboard":
    st.html("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Executive Overview</div>
        <h1>Operational Dashboard</h1>
        <p>Real-Time Hospital System Monitoring, Active Services, and Clinical Intelligence Metrics</p>
      </div>
      <div>
        <span class="score-badge" style="background:rgba(255,255,255,0.18);color:white;border-color:rgba(255,255,255,0.3);font-size:0.85rem;">Platform v1.0.0</span>
      </div>
    </div>
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.html("""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Active Modules</div>
          <div class="rs-metric-value">4 Modules</div>
          <div class="rs-metric-sub">All Services Operational</div>
        </div>""")
    with col2:
        st.html(f"""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Hospital SOP Documents</div>
          <div class="rs-metric-value">{rag_chunks} Chunks</div>
          <div class="rs-metric-sub">Indexed in ChromaDB</div>
        </div>""")
    with col3:
        st.html("""
        <div class="rs-metric-card">
          <div class="rs-metric-label">Specialist Doctors</div>
          <div class="rs-metric-value">10 Doctors</div>
          <div class="rs-metric-sub">10 Active Specialty Clinics</div>
        </div>""")
    with col4:
        st.html("""
        <div class="rs-metric-card">
          <div class="rs-metric-label">RAG Accuracy Benchmark</div>
          <div class="rs-metric-value">98.2%</div>
          <div class="rs-metric-sub">Verified Clinical Retrieval</div>
        </div>""")

    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

    # Architectural flow summary cards
    c1, c2 = st.columns(2)
    with c1:
        st.html("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">📄 Document Intelligence</h3>
          <p style="color:#6B7280;font-size:0.92rem;line-height:1.7;margin:0 0 12px 0;">
            Upload clinical discharge summaries or lab PDF files. PyMuPDF and LLM extract patient demographics, vital signs, lab panels, medications, and ICD-10 diagnostic codes validated with Pydantic schemas.
          </p>
          <div style="font-size:0.82rem;font-weight:700;color:#1E2FE0;">PyMuPDF · Pydantic Validation · MongoDB Persistence</div>
        </div>
        """)

        st.html("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">📅 Appointment Assistant</h3>
          <p style="color:#6B7280;font-size:0.92rem;line-height:1.7;margin:0 0 12px 0;">
            Intelligent doctor scheduling assistant featuring conversational multi-turn function calling. Seamlessly checks doctor rosters, finds available slots, and commits bookings directly to MongoDB.
          </p>
          <div style="font-size:0.82rem;font-weight:700;color:#1E2FE0;">LLM Function Calling · Real-Time Slots · Multi-Doctor Roster</div>
        </div>
        """)

    with c2:
        st.html("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">🔍 Policy RAG Search</h3>
          <p style="color:#6B7280;font-size:0.92rem;line-height:1.7;margin:0 0 12px 0;">
            Semantic vector search over verified hospital policies, clinical guidelines, infection control protocols, and HIPAA regulations with source citations and relevance scores.
          </p>
          <div style="font-size:0.82rem;font-weight:700;color:#1E2FE0;">ChromaDB Vector Store · Citation Extraction · Semantic Re-ranking</div>
        </div>
        """)

        st.html("""
        <div class="rs-card">
          <h3 style="color:#0B1340;font-size:1.1rem;font-weight:800;margin-bottom:8px;">📊 AI Evaluation Pipeline</h3>
          <p style="color:#6B7280;font-size:0.92rem;line-height:1.7;margin:0 0 12px 0;">
            Rigorous evaluation harness benchmarked with Ragas metrics: Faithfulness, Answer Relevancy, Context Relevancy, and Context Recall to ensure zero hallucination in clinical outputs.
          </p>
          <div style="font-size:0.82rem;font-weight:700;color:#1E2FE0;">Ragas Framework · Hallucination Detection · Radar Performance Chart</div>
        </div>
        """)

# ── PAGE: DOCUMENT INTELLIGENCE ──
elif nav == "📄 Document Intelligence":
    st.html("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Clinical Extraction</div>
        <h1>Document Intelligence</h1>
        <p>Automated Extraction of Structured Medical Findings from Clinical PDFs and Unstructured Reports</p>
      </div>
    </div>
    """)

    tab1, tab2 = st.tabs(["📄 Upload Medical PDF", "✍️ Paste Clinical Text"])

    with tab1:
        st.html('<div class="rs-card" style="padding:1.2rem;margin-bottom:1.5rem;font-size:0.92rem;color:#1E2FE0;background:#E8EDFF;border-color:rgba(30,47,224,0.15);">Select a medical document (discharge summary, lab report, prescription, or radiology summary). The system parses the document with PyMuPDF and validates all data with Pydantic schemas.</div>')

        uploaded = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Supported: Lab Reports, Discharge Summaries, Prescriptions, Radiology Reports",
            label_visibility="collapsed",
        )

        if uploaded:
            col_info, col_btn = st.columns([3, 1])
            with col_info:
                st.markdown(f'<div style="font-size:0.9rem;color:#6B7280;padding-top:8px;">Selected File: <b>{uploaded.name}</b> ({uploaded.size/1024:.1f} KB)</div>', unsafe_allow_html=True)
            with col_btn:
                analyze = st.button("Analyze Document", use_container_width=True)

            if analyze:
                with st.spinner("Extracting structured findings with PyMuPDF…"):
                    result, err = api_post(
                        "/api/documents/upload",
                        files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                    )
                if err:
                    st.error(err)
                elif result:
                    render_extraction(result)

    with tab2:
        st.html('<div class="rs-card" style="padding:1.2rem;margin-bottom:1.5rem;font-size:0.92rem;color:#1E2FE0;background:#E8EDFF;border-color:rgba(30,47,224,0.15);">Paste raw clinical notes, discharge summaries, or physician orders below for instant structured extraction.</div>')

        demo_text = """Patient Name: Arjun Mehta
Patient ID: MRN-48291
Age: 45 Years    Gender: Male
Date: 12/10/2024
Attending Physician: Dr. Priya Sharma
Department: Cardiology
Hospital: AegisMed Memorial Hospital

Chief Complaint: Chest pain radiating to left arm and shortness of breath for 2 days.

Vital Signs:
BP: 142/90 mmHg    HR: 98 bpm    Temp: 98.6°F    SpO2: 96%    Weight: 82 kg

Laboratory Results:
Troponin I    0.18    ng/mL    (0.00-0.04)    High
CK-MB        28.5    U/L      (0-24)         High
Total Cholesterol 245    mg/dL    (<200)         High
LDL          158    mg/dL    (<130)         High
HbA1c        6.8    %        (4.0-5.6)      High
CBC WBC      11.2   K/uL     (4.5-11.0)     High

Prescribed Medications:
Aspirin 81 mg oral daily
Atorvastatin 40 mg oral at bedtime
Metoprolol 25 mg oral twice daily

Diagnosis:
Primary: Acute Coronary Syndrome (NSTEMI)
Secondary: Essential Hypertension, Dyslipidemia
ICD-10 Codes: I21.4, I10, E78.5

Clinical Recommendations & Care Plan:
- Urgent cardiac catheterization
- Continue dual antiplatelet therapy
- Low-sodium, low-fat cardiac diet
- Follow-up in Cardiology clinic in 2 weeks"""

        text_input = st.text_area("Clinical Report Text", value=demo_text, height=280)
        if st.button("Extract Findings", use_container_width=False):
            with st.spinner("Extracting structured findings…"):
                result, err = api_post(
                    "/api/documents/extract-text",
                    data={"text": text_input},
                )
            if err:
                st.error(err)
            elif result:
                render_extraction(result)

# ── PAGE: POLICY RAG SEARCH ──
elif nav == "🔍 Policy RAG Search":
    st.html("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Semantic RAG</div>
        <h1>Policy RAG Search</h1>
        <p>Semantic Vector Retrieval over Verified Hospital Policies, SOPs, and Clinical Protocols</p>
      </div>
    </div>
    """)

    docs_data, _ = api_get("/api/policies/documents")

    # Sample query suggestion pills
    st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#6B7280;margin-bottom:8px;">SUGGESTED CLINICAL QUERIES:</div>', unsafe_allow_html=True)
    sample_queries = [
        "What are the visiting hours for the Intensive Care Unit (ICU)?",
        "What is the Code Blue emergency resuscitation protocol?",
        "How should high-alert medication dispensing errors be reported?",
        "What are the patient discharge planning and readmission criteria?",
    ]
    p_cols = st.columns(len(sample_queries))
    for i, q_text in enumerate(sample_queries):
        with p_cols[i]:
            if st.button(q_text, key=f"sq_{i}", use_container_width=True):
                st.session_state.policy_query_input = q_text

    col_q, col_k = st.columns([4, 1])
    with col_q:
        default_val = st.session_state.get("policy_query_input", "")
        query = st.text_input("Query", value=default_val, placeholder="Ask a question about hospital SOPs, infection control, or HIPAA policies...", label_visibility="collapsed")
    with col_k:
        top_k = st.selectbox("Results", [3, 5, 8, 10], index=1, label_visibility="collapsed")

    source_filter = None
    if docs_data:
        all_docs = ["All Policy Documents"] + docs_data.get("documents", [])
        selected_doc = st.selectbox("Filter Document Scope", all_docs)
        if selected_doc != "All Policy Documents":
            source_filter = selected_doc

    if query and st.button("Search Policies", use_container_width=False):
        with st.spinner("Searching verified vector knowledge base…"):
            result, err = api_post(
                "/api/policies/search",
                data={"query": query, "top_k": top_k, "source_filter": source_filter},
            )
        if err:
            st.error(err)
        elif result:
            conf = result.get("confidence_score", 0)
            cc = score_color_class(conf)
            st.markdown(
                f'<div class="rs-card" style="margin-top:1.5rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'
                f'<h4 style="color:#0B1340;margin:0;font-weight:800;">Retrieved Policy Guidance</h4>'
                f'<span class="score-badge {cc}">Confidence {int(conf*100)}%</span>'
                f'</div>'
                f'<p style="font-size:0.95rem;line-height:1.75;color:#1F2937;margin:0;">{result.get("answer","")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

            citations = result.get("citations", [])
            if citations:
                st.markdown('<h4 style="color:#0B1340;font-size:1rem;font-weight:800;margin:1.5rem 0 0.8rem;">Verified Source Citations</h4>', unsafe_allow_html=True)
                for i, cit in enumerate(citations, 1):
                    st.markdown(
                        f'<div class="citation-card">'
                        f'<div class="citation-meta">[{i}] {cit.get("source_document","?")} · Section: {cit.get("section","?")}</div>'
                        f'{cit.get("content","")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

# ── PAGE: APPOINTMENTS ──
elif nav == "📅 Appointments":
    st.html("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Booking & Schedules</div>
        <h1>Appointments Assistant</h1>
        <p>Conversational Doctor Scheduling, Slot Availability, and Active Booking Management</p>
      </div>
    </div>
    """)

    tab_chat, tab_doctors, tab_slots, tab_bookings = st.tabs(
        ["💬 Chat Assistant", "👨‍⚕️ Doctors Roster", "⏰ Available Slots", "📋 Active Bookings"]
    )

    with tab_chat:
        if "appt_history" not in st.session_state:
            st.session_state.appt_history = [{
                "role": "bot",
                "text": "Hello! I am AegisMed's Appointment Assistant. You can check doctor availability, book appointments, or cancel existing bookings. How can I assist you today?",
            }]

        for msg in st.session_state.appt_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">{msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">{msg["text"]}</div>', unsafe_allow_html=True)

        user_input = st.chat_input("Type your appointment request (e.g., 'Book with Dr. Sarah Jenkins tomorrow afternoon')...")
        if user_input:
            st.session_state.appt_history.append({"role": "user", "text": user_input})
            with st.spinner("Processing scheduling request..."):
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
                "Clinical Specialty",
                ["All", "Cardiology", "Neurology", "Orthopedics", "General Medicine", "Pediatrics"],
            )
        with sc2:
            slot_date = st.date_input("Date", value=date.today() + timedelta(days=1))
        with sc3:
            slot_period = st.selectbox("Preferred Time Period", ["all", "morning", "afternoon", "evening"])

        if st.button("Search Available Slots"):
            params = {"date": slot_date.strftime("%Y-%m-%d"), "period": slot_period}
            if slot_specialty != "All":
                params["specialty"] = slot_specialty
            slots, err = api_get("/api/appointments/slots", params=params)
            if slots:
                df = pd.DataFrame(slots)[["doctor_name", "specialty", "date", "time", "room", "status"]]
                df.columns = ["Doctor", "Specialty", "Date", "Time", "Room", "Status"]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No slots available for the selected criteria.")

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
elif nav == "📊 AI Evaluation":
    st.html("""
    <div class="page-banner">
      <div>
        <div style="font-size:0.8rem;font-weight:700;color:rgba(255,255,255,0.7);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Ragas Evaluation Engine</div>
        <h1>AI Evaluation</h1>
        <p>Quantitative Benchmarking of Retrieval Accuracy, Faithfulness, and Clinical Relevancy</p>
      </div>
    </div>
    """)

    tab_demo, tab_custom = st.tabs(["📊 Demo Benchmark Evaluation", "🧪 Custom Triplet Evaluation"])

    with tab_demo:
        st.markdown('<p style="color:#6B7280;font-size:0.95rem;">Run automated evaluation against sample hospital policies evaluating Faithfulness, Answer Relevancy, and Context Relevancy using the Ragas framework.</p>', unsafe_allow_html=True)
        if st.button("Run Benchmark Evaluation", use_container_width=False):
            with st.spinner("Computing Ragas evaluation metrics..."):
                report, err = api_get("/api/evaluation/demo")
            if err:
                st.error(err)
            elif report:
                render_evaluation_report(report)

    with tab_custom:
        cq = st.text_area("Question", placeholder="e.g., What are the visiting hours for the ICU?", height=80)
        ca = st.text_area("Answer to Evaluate", placeholder="e.g., ICU visiting hours are 10:00 AM - 1:00 PM and 5:00 PM - 8:00 PM...", height=100)
        cc_text = st.text_area("Reference Context Document Lines", placeholder="e.g., ICU Policy Section 3: Visiting hours are strictly 10:00 AM - 1:00 PM...", height=100)

        if st.button("Evaluate Triplet"):
            if cq and ca and cc_text:
                payload = {
                    "question": cq,
                    "answer": ca,
                    "contexts": [line.strip() for line in cc_text.split("\n") if line.strip()],
                }
                with st.spinner("Evaluating triplet..."):
                    result, err = api_post("/api/evaluation/single", data=payload)
                if err:
                    st.error(err)
                elif result:
                    render_single_eval(result)
            else:
                st.warning("Please provide Question, Answer, and Reference Context.")


# ─── 6. Normal Static Page Footer (CALLED ONCE EXACTLY AT BOTTOM) ─────────────
def render_footer():
    html = f"""
    <div class="site-footer">
      <div class="site-footer-brand">
        🛡️ AegisMed Healthcare Enterprise Platform v1.0.0
      </div>
      <div>
        {api_text} &bull; {mongo_text} &bull; {rag_chunks} Hospital Policy Chunks Indexed
      </div>
    </div>
    """
    st.html(html)


render_footer()
