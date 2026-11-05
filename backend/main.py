"""
🛡️ AegisMed — FastAPI Backend Application
Main entry point with all four module routers.
"""
import os
import uuid
import logging
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.config import settings
from backend.modules.document_intelligence import (
    DocumentIntelligenceService, MedicalDocumentExtraction
)
from backend.modules.policy_rag import PolicyRAGService, PolicySearchResult
from backend.modules.appointment_assistant import (
    AppointmentAssistantService, AppointmentResponse, TimeSlot
)
from backend.modules.evaluation_pipeline import (
    EvaluationService, EvaluationSample, EvaluationResult, BatchEvaluationReport
)
from backend.database import db_manager

# ─── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("sevaai")


# ─── Service Singletons ───────────────────────────────────────────────────────
_doc_service: Optional[DocumentIntelligenceService] = None
_rag_service: Optional[PolicyRAGService] = None
_appt_service: Optional[AppointmentAssistantService] = None
_eval_service: Optional[EvaluationService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize all services and seed policies on startup."""
    global _doc_service, _rag_service, _appt_service, _eval_service

    logger.info("🏥 🛡️ AegisMed starting up...")

    # Connect to MongoDB (with fallback error handling if offline)
    await db_manager.connect()

    _doc_service  = DocumentIntelligenceService()
    _rag_service  = PolicyRAGService(
        persist_dir=settings.chroma_persist_dir,
        openai_api_key=settings.openai_api_key,
    )
    _appt_service = AppointmentAssistantService(
        openai_api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    _eval_service = EvaluationService(
        openai_api_key=settings.openai_api_key,
    )

    # Auto-seed policies if ChromaDB is empty
    stats = _rag_service.get_stats()
    if stats["total_chunks"] == 0:
        logger.info("ChromaDB is empty — seeding hospital policies...")
        try:
            from backend.seed_policies import seed_policies
            seed_policies()
        except Exception as e:
            logger.warning(f"Auto-seeding failed: {e}")

    logger.info("✅ 🛡️ AegisMed backend ready!")
    yield
    await db_manager.disconnect()
    logger.info("🛡️ AegisMed shutting down.")


# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="🛡️ AegisMed — Hospital Administration Assistant",
    description=(
        "AI-powered hospital administration API with Document Intelligence, "
        "Policy RAG Search, Appointment Assistant, and AI Evaluation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "modules": ["document_intelligence", "policy_rag", "appointment_assistant", "evaluation"],
        "rag_stats": _rag_service.get_stats() if _rag_service else {},
        "mongodb": {
            "connected": db_manager.is_connected,
            "database": settings.mongodb_db_name if db_manager.is_connected else None,
        },
    }


# ─── Module 1: Document Intelligence ─────────────────────────────────────────

@app.post(
    "/api/documents/upload",
    response_model=MedicalDocumentExtraction,
    tags=["Document Intelligence"],
    summary="Upload & parse a medical PDF",
)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a medical PDF. 🛡️ AegisMed extracts structured key-value findings
    validated against the MedicalDocumentExtraction Pydantic schema.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    doc_id = str(uuid.uuid4())[:8].upper()
    upload_path = Path(settings.upload_dir) / f"{doc_id}_{file.filename}"

    try:
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        result = _doc_service.extract_from_pdf(str(upload_path), doc_id)
        # Persist extraction log to MongoDB (fallback safe)
        await db_manager.save_document_extraction(result.model_dump())
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        raise HTTPException(status_code=422, detail=f"Extraction failed: {e}")

    return result


class TextExtractionRequest(BaseModel):
    text: str
    doc_id: Optional[str] = None


@app.post(
    "/api/documents/extract-text",
    response_model=MedicalDocumentExtraction,
    tags=["Document Intelligence"],
    summary="Extract structured data from raw medical text",
)
async def extract_from_text(req: TextExtractionRequest):
    """Extract structured medical data from pasted raw text."""
    doc_id = req.doc_id or str(uuid.uuid4())[:8].upper()
    try:
        result = _doc_service.extract_from_text(req.text, doc_id)
        # Persist extraction log to MongoDB (fallback safe)
        await db_manager.save_document_extraction(result.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get(
    "/api/documents/logs",
    tags=["Document Intelligence"],
    summary="Get recent document extraction logs from MongoDB",
)
async def get_document_logs(limit: int = Query(50, ge=1, le=200)):
    """Retrieve document extraction logs stored in MongoDB."""
    extractions = await db_manager.get_document_extractions(limit=limit)
    return {
        "total": len(extractions),
        "source": "mongodb" if db_manager.is_connected else "fallback_empty",
        "extractions": extractions,
    }


# ─── Module 2: Policy RAG Search ──────────────────────────────────────────────

class PolicyQueryRequest(BaseModel):
    query: str
    top_k: int = 5
    source_filter: Optional[str] = None


@app.post(
    "/api/policies/search",
    response_model=PolicySearchResult,
    tags=["Policy RAG"],
    summary="Semantic search over hospital policies",
)
async def search_policies(req: PolicyQueryRequest):
    """
    Perform RAG-based semantic search over indexed hospital policy documents.
    Returns an answer with strict source citations.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        result = _rag_service.search(
            query=req.query,
            top_k=req.top_k,
            source_filter=req.source_filter,
        )
        return result
    except Exception as e:
        logger.error(f"Policy search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/policies/documents",
    tags=["Policy RAG"],
    summary="List indexed policy documents",
)
async def list_policy_documents():
    """List all policy documents currently indexed in ChromaDB."""
    return {
        "documents": _rag_service.list_indexed_documents(),
        "stats": _rag_service.get_stats(),
    }


@app.post(
    "/api/policies/reseed",
    tags=["Policy RAG"],
    summary="Re-seed policy database",
)
async def reseed_policies():
    """Re-index all built-in hospital policy documents."""
    try:
        from backend.seed_policies import seed_policies
        seed_policies()
        return {"status": "success", "stats": _rag_service.get_stats()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Module 3: Appointment Assistant ─────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str


@app.post(
    "/api/appointments/chat",
    response_model=AppointmentResponse,
    tags=["Appointments"],
    summary="Natural-language appointment assistant",
)
async def appointment_chat(req: ChatRequest):
    """
    Chat with the appointment assistant. Supports availability queries,
    slot booking, and cancellations via LLM function calling.
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    try:
        result = _appt_service.chat(req.message)

        # Store booking to MongoDB if an appointment was booked
        if result.booking_confirmation:
            await db_manager.save_booking(result.booking_confirmation.model_dump())

        # If it was a cancellation confirmed, update booking in MongoDB
        if result.intent == "cancellation_confirmed":
            import re
            match = re.search(r"BK-\d+", result.message)
            if match:
                await db_manager.update_booking_status(match.group(0), "cancelled")

        return result
    except Exception as e:
        logger.error(f"Appointment chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/appointments/doctors",
    tags=["Appointments"],
    summary="List all doctors",
)
async def list_doctors():
    """Return full doctor roster with specialties."""
    return {"doctors": _appt_service.get_all_doctors()}


@app.get(
    "/api/appointments/bookings",
    tags=["Appointments"],
    summary="List all current bookings",
)
async def list_bookings():
    """Return appointment bookings from MongoDB or fallback to in-memory bookings."""
    if db_manager.is_connected:
        db_bookings = await db_manager.get_bookings()
        if db_bookings:
            return {"source": "mongodb", "bookings": db_bookings}
    return {"source": "in_memory", "bookings": [b.model_dump() for b in _appt_service.get_bookings()]}


@app.get(
    "/api/appointments/slots",
    tags=["Appointments"],
    response_model=List[TimeSlot],
    summary="Query available slots",
)
async def get_slots(
    specialty: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    period: str = Query("all"),
):
    """Query available appointment slots directly."""
    from backend.modules.appointment_assistant import DOCTORS_DB, _get_available_slots
    from datetime import date as dt, timedelta

    target = date or (dt.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    all_slots = []
    for dr_id, dr in DOCTORS_DB.items():
        if specialty and dr["specialty"].lower() != specialty.lower():
            continue
        from backend.modules.appointment_assistant import AppointmentStatus
        slots = _get_available_slots(dr_id, target, period)
        all_slots.extend([s for s in slots if s.status == AppointmentStatus.AVAILABLE][:3])
    return all_slots[:20]


# ─── Module 4: AI Evaluation ──────────────────────────────────────────────────

@app.post(
    "/api/evaluation/single",
    response_model=EvaluationResult,
    tags=["AI Evaluation"],
    summary="Evaluate a single Q&A pair",
)
async def evaluate_single(sample: EvaluationSample):
    """
    Evaluate a single question-answer-context triplet using Ragas metrics.
    Returns faithfulness, answer relevancy, and context relevancy scores.
    """
    try:
        result = _eval_service.evaluate_single(sample)
        # Store evaluation result to MongoDB
        await db_manager.save_evaluation_result(result.model_dump())
        return result
    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/api/evaluation/batch",
    response_model=BatchEvaluationReport,
    tags=["AI Evaluation"],
    summary="Evaluate a batch of Q&A pairs",
)
async def evaluate_batch(samples: List[EvaluationSample]):
    """Evaluate multiple Q&A pairs and return aggregated metrics."""
    if not samples:
        raise HTTPException(status_code=400, detail="No samples provided.")
    try:
        report = _eval_service.evaluate_batch(samples)
        # Store batch evaluation report to MongoDB
        await db_manager.save_batch_evaluation(report.model_dump())
        return report
    except Exception as e:
        logger.error(f"Batch evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/evaluation/demo",
    response_model=BatchEvaluationReport,
    tags=["AI Evaluation"],
    summary="Run demo evaluation with pre-built samples",
)
async def run_demo_evaluation():
    """Run the evaluation pipeline on pre-built hospital policy Q&A samples."""
    try:
        samples = _eval_service.get_sample_evaluations()
        report = _eval_service.evaluate_batch(samples)
        # Store demo batch evaluation report to MongoDB
        await db_manager.save_batch_evaluation(report.model_dump())
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/api/evaluation/history",
    tags=["AI Evaluation"],
    summary="Get evaluation history from MongoDB",
)
async def get_evaluation_history(limit: int = Query(50, ge=1, le=200)):
    """Retrieve stored evaluation results from MongoDB."""
    results = await db_manager.get_evaluation_results(limit=limit)
    return {
        "total": len(results),
        "source": "mongodb" if db_manager.is_connected else "fallback_empty",
        "results": results,
    }
