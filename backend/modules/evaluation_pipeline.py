"""
Module 4: AI Evaluation Pipeline
Uses Ragas to measure answer faithfulness and context relevance.
Falls back to heuristic scoring when OpenAI is not configured.
"""
from __future__ import annotations
import re
import time
import logging
import math
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ─── Data Models ──────────────────────────────────────────────────────────────

class EvaluationSample(BaseModel):
    question: str
    answer: str
    contexts: List[str]
    ground_truth: Optional[str] = None


class EvaluationMetrics(BaseModel):
    faithfulness: float = Field(ge=0.0, le=1.0, description="How grounded answer is in context")
    answer_relevancy: float = Field(ge=0.0, le=1.0, description="How relevant answer is to question")
    context_relevancy: float = Field(ge=0.0, le=1.0, description="How relevant context is to question")
    context_recall: Optional[float] = Field(None, ge=0.0, le=1.0, description="Requires ground_truth")
    overall_score: float = Field(ge=0.0, le=1.0)


class EvaluationResult(BaseModel):
    sample: EvaluationSample
    metrics: EvaluationMetrics
    evaluation_mode: str  # "ragas" | "heuristic"
    duration_seconds: float
    notes: List[str] = []


class BatchEvaluationReport(BaseModel):
    total_samples: int
    avg_faithfulness: float
    avg_answer_relevancy: float
    avg_context_relevancy: float
    avg_overall_score: float
    results: List[EvaluationResult]
    evaluation_mode: str
    duration_seconds: float


# ─── Heuristic Scorer (No LLM required) ───────────────────────────────────────

def _tokenize(text: str) -> set:
    """Simple word-level tokenizer."""
    return set(re.findall(r"\b[a-z]{2,}\b", text.lower()))


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _faithfulness_heuristic(answer: str, contexts: List[str]) -> float:
    """
    Heuristic: what fraction of answer sentences are supported by context.
    """
    sentences = [s.strip() for s in re.split(r"[.!?]", answer) if len(s.strip()) > 10]
    if not sentences:
        return 0.5

    context_text = " ".join(contexts)
    context_tokens = _tokenize(context_text)
    supported = 0

    for sent in sentences:
        sent_tokens = _tokenize(sent)
        if not sent_tokens:
            continue
        overlap = len(sent_tokens & context_tokens) / len(sent_tokens)
        if overlap >= 0.3:
            supported += 1

    return round(supported / len(sentences), 3)


def _answer_relevancy_heuristic(question: str, answer: str) -> float:
    """
    Heuristic: keyword overlap between question and answer.
    """
    q_tokens = _tokenize(question)
    a_tokens = _tokenize(answer)
    # Remove stopwords
    stopwords = {"the", "is", "are", "was", "what", "how", "when", "where", "who", "why", "a", "an", "in", "of", "to"}
    q_tokens -= stopwords
    a_tokens -= stopwords
    if not q_tokens:
        return 0.5
    overlap = len(q_tokens & a_tokens) / len(q_tokens)
    # Bonus for answer length (very short answers are less relevant)
    length_bonus = min(1.0, len(answer.split()) / 30) * 0.2
    return round(min(1.0, overlap * 0.8 + length_bonus), 3)


def _context_relevancy_heuristic(question: str, contexts: List[str]) -> float:
    """
    Heuristic: average Jaccard similarity between question and each context chunk.
    """
    if not contexts:
        return 0.0
    q_tokens = _tokenize(question)
    scores = [_jaccard(q_tokens, _tokenize(ctx)) for ctx in contexts]
    return round(sum(scores) / len(scores), 3)


def _context_recall_heuristic(ground_truth: str, contexts: List[str]) -> float:
    """
    Heuristic: how much of ground truth is covered in context.
    """
    if not ground_truth or not contexts:
        return 0.0
    gt_tokens = _tokenize(ground_truth)
    ctx_tokens = _tokenize(" ".join(contexts))
    if not gt_tokens:
        return 0.0
    return round(len(gt_tokens & ctx_tokens) / len(gt_tokens), 3)


# ─── Evaluation Service ───────────────────────────────────────────────────────

class EvaluationService:
    """
    AI Evaluation pipeline using Ragas (with OpenAI) or heuristic fallback.
    Measures faithfulness, answer relevancy, and context relevancy.
    """

    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self._use_mock = not (openai_api_key and openai_api_key != "your_openai_api_key_here")
        self._ragas_available = False

        if not self._use_mock:
            try:
                import ragas
                from ragas.metrics import faithfulness, answer_relevancy, context_relevancy
                self._ragas_available = True
                logger.info("Ragas evaluation enabled with OpenAI")
            except ImportError:
                logger.warning("Ragas not installed; using heuristic fallback")

    def evaluate_single(self, sample: EvaluationSample) -> EvaluationResult:
        """Evaluate a single Q&A sample."""
        start = time.time()

        if self._ragas_available and not self._use_mock:
            return self._ragas_evaluate(sample, start)
        return self._heuristic_evaluate(sample, start)

    def evaluate_batch(self, samples: List[EvaluationSample]) -> BatchEvaluationReport:
        """Evaluate a batch of Q&A samples."""
        start = time.time()
        results = [self.evaluate_single(s) for s in samples]

        avg = lambda key: round(
            sum(getattr(r.metrics, key) for r in results) / len(results), 3
        ) if results else 0.0

        return BatchEvaluationReport(
            total_samples=len(results),
            avg_faithfulness=avg("faithfulness"),
            avg_answer_relevancy=avg("answer_relevancy"),
            avg_context_relevancy=avg("context_relevancy"),
            avg_overall_score=avg("overall_score"),
            results=results,
            evaluation_mode="ragas" if self._ragas_available else "heuristic",
            duration_seconds=round(time.time() - start, 2),
        )

    def _heuristic_evaluate(
        self, sample: EvaluationSample, start: float
    ) -> EvaluationResult:
        faithfulness_score  = _faithfulness_heuristic(sample.answer, sample.contexts)
        answer_rel          = _answer_relevancy_heuristic(sample.question, sample.answer)
        context_rel         = _context_relevancy_heuristic(sample.question, sample.contexts)
        context_rec         = (
            _context_recall_heuristic(sample.ground_truth, sample.contexts)
            if sample.ground_truth else None
        )

        overall = round(
            (faithfulness_score * 0.35 + answer_rel * 0.35 + context_rel * 0.30),
            3
        )

        metrics = EvaluationMetrics(
            faithfulness=faithfulness_score,
            answer_relevancy=answer_rel,
            context_relevancy=context_rel,
            context_recall=context_rec,
            overall_score=overall,
        )

        return EvaluationResult(
            sample=sample,
            metrics=metrics,
            evaluation_mode="heuristic",
            duration_seconds=round(time.time() - start, 3),
            notes=[
                "Heuristic mode: scores based on token overlap (no LLM required).",
                "Configure OPENAI_API_KEY and install ragas for full LLM-based evaluation.",
            ],
        )

    def _ragas_evaluate(
        self, sample: EvaluationSample, start: float
    ) -> EvaluationResult:
        """Full Ragas evaluation with OpenAI."""
        try:
            from ragas import evaluate
            from ragas.metrics import (
                faithfulness, answer_relevancy, context_relevancy, context_recall
            )
            from datasets import Dataset
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings

            llm = ChatOpenAI(api_key=self.openai_api_key, model="gpt-4o-mini", temperature=0)
            embeddings = OpenAIEmbeddings(api_key=self.openai_api_key, model="text-embedding-3-small")

            data = {
                "question":  [sample.question],
                "answer":    [sample.answer],
                "contexts":  [sample.contexts],
            }
            metrics_list = [faithfulness, answer_relevancy, context_relevancy]

            if sample.ground_truth:
                data["ground_truth"] = [sample.ground_truth]
                metrics_list.append(context_recall)

            dataset = Dataset.from_dict(data)
            result = evaluate(
                dataset,
                metrics=metrics_list,
                llm=llm,
                embeddings=embeddings,
            )
            df = result.to_pandas()
            row = df.iloc[0]

            metrics = EvaluationMetrics(
                faithfulness=float(row.get("faithfulness", 0.0)),
                answer_relevancy=float(row.get("answer_relevancy", 0.0)),
                context_relevancy=float(row.get("context_relevancy", 0.0)),
                context_recall=float(row["context_recall"]) if "context_recall" in row else None,
                overall_score=round(
                    float(row.get("faithfulness", 0)) * 0.35
                    + float(row.get("answer_relevancy", 0)) * 0.35
                    + float(row.get("context_relevancy", 0)) * 0.30,
                    3,
                ),
            )
            return EvaluationResult(
                sample=sample,
                metrics=metrics,
                evaluation_mode="ragas",
                duration_seconds=round(time.time() - start, 2),
            )

        except Exception as e:
            logger.error(f"Ragas evaluation failed: {e}. Falling back to heuristic.")
            return self._heuristic_evaluate(sample, start)

    def get_sample_evaluations(self) -> List[EvaluationSample]:
        """Return pre-built sample evaluation pairs for the demo dashboard."""
        return [
            EvaluationSample(
                question="What is the hospital's policy on patient data privacy?",
                answer=(
                    "All patient data is handled in strict compliance with HIPAA regulations. "
                    "Medical records are stored encrypted and access is restricted to authorized personnel only. "
                    "Patients have the right to request their records at any time."
                ),
                contexts=[
                    "🛡️ AegisMed Hospital follows HIPAA-compliant data management protocols. All electronic health records (EHRs) are encrypted using AES-256.",
                    "Access to patient data is role-based. Only treating physicians, nursing staff, and administrative staff with appropriate clearance can view records.",
                    "Patients may submit a written request for their medical records within 30 business days of discharge.",
                ],
                ground_truth="Patient data is protected under HIPAA, stored encrypted, and accessible only to authorized staff.",
            ),
            EvaluationSample(
                question="What are the visiting hours for ICU patients?",
                answer=(
                    "ICU visiting hours are 10 AM – 12 PM and 4 PM – 6 PM daily. "
                    "Only two visitors are allowed at a time. Children under 12 are not permitted."
                ),
                contexts=[
                    "Intensive Care Unit (ICU) visiting policy: Visiting hours 10:00 AM to 12:00 PM and 4:00 PM to 6:00 PM.",
                    "Maximum two visitors per patient at any time in ICU.",
                    "Children under 12 years of age are not allowed in ICU or NICU wards.",
                ],
                ground_truth="ICU visiting hours are 10 AM–12 PM and 4–6 PM, max 2 visitors, no children under 12.",
            ),
            EvaluationSample(
                question="How does the hospital handle medication dispensing errors?",
                answer=(
                    "Medication errors must be reported immediately to the charge nurse and pharmacist. "
                    "An incident report is filed within 1 hour. The patient is monitored for adverse effects."
                ),
                contexts=[
                    "Any medication dispensing error must be immediately reported to the charge nurse.",
                    "A formal incident report must be completed within 60 minutes of error discovery.",
                    "The patient must be continuously monitored for adverse reactions following a dispensing error.",
                    "The pharmacy department conducts a root cause analysis within 24 hours.",
                ],
            ),
        ]
