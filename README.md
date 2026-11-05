# 🛡️ AegisMed — AI Hospital Administration Assistant

<div align="center">

```
    _              _     __  __           _ 
   / \   ___  __ _(_)___|  \/  | ___   __| |
  / _ \ / _ \/ _` | / __| |\/| |/ _ \ / _` |
 / ___ \  __/ (_| | \__ \ |  | |  __/| (_| |
/_/   \_\___|\__, |_|___/_|  |_|\___(_)__,_|
             |___/                          

AI Hospital Administration Assistant
```

**FastAPI · ChromaDB · Streamlit · PyMuPDF · Ragas**

</div>

---

## 🏥 Overview

**🛡️ AegisMed** is a full-stack, single-repository MVP for an AI-powered Hospital Administration Assistant featuring four production-ready modules:

| Module | Description | Technology |
|--------|-------------|------------|
| 📄 Document Intelligence | Parse & extract structured data from medical PDFs | PyMuPDF + Pydantic v2 |
| 🔍 Policy RAG Search | Semantic search with strict source citations | ChromaDB + LangChain |
| 📅 Appointment Assistant | NL booking via LLM function calling | OpenAI Functions (mock fallback) |
| 📊 AI Evaluation | Faithfulness & relevancy scoring | Ragas (heuristic fallback) |

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
cd "AI Hospital"

# Automated setup (recommended)
bash scripts/setup_and_verify.sh
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY (optional — mock mode works without it)
```

### 3. Run the Application

```bash
# Option A: Run both services at once
bash scripts/run_all.sh

# Option B: Run individually
source .venv/bin/activate

# Terminal 1 — Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend
streamlit run frontend/app.py
```

### 4. Access the Application

| Service | URL |
|---------|-----|
| 🖥️ Streamlit Dashboard | http://localhost:8501 |
| 📡 FastAPI Backend | http://localhost:8000 |
| 📖 API Documentation | http://localhost:8000/docs |
| 🔁 ReDoc | http://localhost:8000/redoc |

---

## 📂 Project Structure

```
AI Hospital/
├── backend/
│   ├── __init__.py
│   ├── config.py                    # Pydantic settings
│   ├── main.py                      # FastAPI app + all routers
│   ├── seed_policies.py             # Policy database seeder
│   └── modules/
│       ├── __init__.py
│       ├── document_intelligence.py # Module 1: PDF parsing
│       ├── policy_rag.py            # Module 2: ChromaDB RAG
│       ├── appointment_assistant.py # Module 3: LLM booking
│       └── evaluation_pipeline.py  # Module 4: Ragas eval
├── frontend/
│   └── app.py                       # Streamlit dashboard
├── scripts/
│   ├── setup_and_verify.sh         # Setup & verification
│   └── run_all.sh                  # Start all services
├── data/
│   ├── uploads/                    # Uploaded PDFs
│   ├── chroma_db/                  # ChromaDB persistence
│   └── policies/                   # Policy document store
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
└── README.md
```

---

## 🔧 Module Details

### 1. 📄 Document Intelligence

Parses uploaded medical PDFs using **PyMuPDF** and extracts structured data:

- **Patient Info**: Name, ID, age, gender, attending physician, department
- **Vital Signs**: BP, HR, temperature, SpO2, weight, height, BMI
- **Lab Results**: Test name, value, unit, reference range, status (High/Low/Normal)
- **Medications**: Name, dosage, frequency, route, duration
- **Diagnosis**: Primary, secondary, ICD-10 codes
- **Recommendations**: Follow-up instructions

All data is validated through **Pydantic v2 schemas** with confidence scoring.

**API Endpoints:**
```
POST /api/documents/upload        # Upload PDF
POST /api/documents/extract-text  # Parse raw text
```

### 2. 🔍 Hospital Policy RAG Search

Semantic search over **8 built-in hospital policy documents**:

- Patient Rights & Responsibilities
- HIPAA Data Privacy Policy
- ICU Visiting Hours Policy
- Medication Safety & Dispensing
- Emergency Response & Code Blue
- Infection Control & Hand Hygiene
- Patient Discharge Planning
- Billing & Insurance Policy

Every answer includes **strict source citations** with document name, section, and chunk ID.

**API Endpoints:**
```
POST /api/policies/search     # Semantic search with citations
GET  /api/policies/documents  # List indexed documents
POST /api/policies/reseed     # Re-index all policies
```

### 3. 📅 Appointment Assistant

Natural-language appointment management with **LLM function calling**:

- 10 specialist doctors across 10 medical specialties
- Mock slot generation with morning/afternoon/evening sessions
- Full conversation: query → select → book → confirm → cancel
- Falls back to deterministic rule-based logic without OpenAI

**API Endpoints:**
```
POST /api/appointments/chat      # NL chat interface
GET  /api/appointments/doctors   # List all doctors
GET  /api/appointments/slots     # Query available slots
GET  /api/appointments/bookings  # List bookings
```

### 4. 📊 AI Evaluation Pipeline

Evaluates RAG answers using **Ragas metrics**:

| Metric | Description |
|--------|-------------|
| Faithfulness | Fraction of answer claims supported by context |
| Answer Relevancy | How relevant the answer is to the question |
| Context Relevancy | How relevant the retrieved context is |
| Context Recall | Ground truth coverage in context (requires GT) |

Falls back to **heuristic token-overlap scoring** when OpenAI is not configured.

**API Endpoints:**
```
POST /api/evaluation/single  # Evaluate one Q&A pair
POST /api/evaluation/batch   # Evaluate multiple pairs
GET  /api/evaluation/demo    # Run pre-built demo samples
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | `your_key_here` | OpenAI API key (optional) |
| `OPENAI_MODEL` | `gpt-4o-mini` | LLM model for appointments/eval |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model for RAG |
| `CHROMA_PERSIST_DIR` | `./data/chroma_db` | ChromaDB storage path |
| `UPLOAD_DIR` | `./data/uploads` | PDF upload directory |
| `API_PORT` | `8000` | FastAPI server port |

---

## 🎯 Mock Mode (No OpenAI Required)

🛡️ AegisMed runs **fully offline** without an OpenAI API key:

- **Document Intelligence**: Pure regex + PyMuPDF (no LLM)
- **Policy RAG**: ChromaDB with default hash-based embeddings
- **Appointments**: Deterministic rule-based NL understanding
- **Evaluation**: Heuristic token-overlap scoring (Jaccard similarity)

---

## 🩺 Sample Queries

**Document Intelligence:**
> Upload any medical PDF or paste this demo lab report text

**Policy RAG:**
> "What are the ICU visiting hours?"
> "How should medication errors be reported?"
> "What is the HIPAA breach notification timeline?"

**Appointments:**
> "Show me available Cardiology slots tomorrow"
> "Book an appointment with Dr. Sharma for patient Ravi Kumar"
> "Cancel booking BK-12345"

**Evaluation:**
> Use the demo evaluation tab to auto-run 3 pre-built hospital policy Q&A samples

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.115.5 | Backend API framework |
| uvicorn | 0.32.1 | ASGI server |
| streamlit | 1.40.2 | Dashboard UI |
| PyMuPDF | 1.24.14 | PDF parsing |
| chromadb | 0.5.23 | Vector store |
| pydantic | 2.10.3 | Data validation |
| pydantic-settings | 2.6.1 | Config management |
| openai | 1.55.3 | LLM + embeddings |
| ragas | 0.2.7 | RAG evaluation |
| plotly | 5.24.1 | Visualizations |

---

<div align="center">
Built with ❤️ for healthcare · 🛡️ AegisMed v1.0.0
</div>
