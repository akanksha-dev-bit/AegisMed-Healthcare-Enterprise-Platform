"""
Module 1: Document Intelligence
Parses uploaded medical PDFs using PyMuPDF and extracts structured
key-value findings validated through Pydantic schemas.
"""
from __future__ import annotations
import fitz  # PyMuPDF
import re
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import date, datetime
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class VitalSigns(BaseModel):
    blood_pressure: Optional[str] = Field(None, description="e.g. 120/80 mmHg")
    heart_rate: Optional[str] = Field(None, description="e.g. 72 bpm")
    temperature: Optional[str] = Field(None, description="e.g. 98.6 °F")
    oxygen_saturation: Optional[str] = Field(None, description="e.g. 98%")
    respiratory_rate: Optional[str] = Field(None, description="e.g. 16 breaths/min")
    weight: Optional[str] = Field(None, description="e.g. 70 kg")
    height: Optional[str] = Field(None, description="e.g. 175 cm")
    bmi: Optional[str] = Field(None, description="e.g. 22.9")


class LabResult(BaseModel):
    test_name: str
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = Field(None, description="Normal / High / Low / Critical")


class Medication(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    duration: Optional[str] = None


class Diagnosis(BaseModel):
    primary: Optional[str] = None
    secondary: List[str] = []
    icd_codes: List[str] = []


class MedicalDocumentExtraction(BaseModel):
    """Complete structured extraction from a medical document."""
    document_id: str
    document_type: str = Field(
        description="e.g. Lab Report, Discharge Summary, Prescription, Radiology Report"
    )
    patient_name: Optional[str] = None
    patient_id: Optional[str] = None
    patient_age: Optional[str] = None
    patient_gender: Optional[str] = None
    date_of_report: Optional[str] = None
    attending_physician: Optional[str] = None
    department: Optional[str] = None
    hospital_name: Optional[str] = None

    vital_signs: VitalSigns = Field(default_factory=VitalSigns)
    lab_results: List[LabResult] = []
    medications: List[Medication] = []
    diagnosis: Diagnosis = Field(default_factory=Diagnosis)
    chief_complaint: Optional[str] = None
    clinical_notes: Optional[str] = None
    recommendations: List[str] = []
    follow_up_date: Optional[str] = None

    raw_text_length: int = 0
    pages_processed: int = 0
    extraction_confidence: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Confidence score 0–1"
    )


# ─── Extraction Helpers ───────────────────────────────────────────────────────

PATTERNS = {
    "patient_name":     [r"Patient(?:\s+Name)?[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
                         r"Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)"],
    "patient_id":       [r"(?:Patient\s+)?ID[:\s#]+(\w+[-/]?\w+)",
                         r"MRN[:\s]+(\w+)"],
    "patient_age":      [r"Age[:\s]+(\d{1,3})\s*(?:yrs?|years?)?",
                         r"(\d{1,3})\s*(?:year[s]?\s+old|Y/O)"],
    "patient_gender":   [r"(?:Gender|Sex)[:\s]+(Male|Female|Other|M|F)",
                         r"\b(Male|Female)\b"],
    "date_of_report":   [r"(?:Date|Report\s+Date|Date\s+of\s+Report)[:\s]+([\d/\-\.]+)",
                         r"(\d{2}[/-]\d{2}[/-]\d{4})"],
    "attending_physician": [r"(?:Dr\.?\s+|Physician[:\s]+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
                            r"(?:Attending|Consultant)[:\s]+(?:Dr\.?\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)"],
    "hospital_name":    [r"(?:Hospital|Clinic|Medical\s+Center)[:\s]+([^\n]+)",
                         r"^([A-Z][^\n]+(?:Hospital|Clinic|Medical))[^\n]*$"],
    "department":       [r"(?:Department|Dept\.?)[:\s]+([^\n]+)",
                         r"(?:Ward|Unit)[:\s]+([^\n]+)"],
    "chief_complaint":  [r"(?:Chief\s+Complaint|CC|Presenting\s+Complaint)[:\s]+([^\n]+)"],
    "follow_up_date":   [r"(?:Follow[- ]?up|Next\s+Visit)[:\s]+([\d/\-\.]+\s*(?:days?|weeks?|months?)?)",
                         r"Return\s+in\s+(\d+\s+(?:days?|weeks?|months?))"],
}

VITAL_PATTERNS = {
    "blood_pressure":   r"(?:BP|Blood\s+Pressure)[:\s]+([\d/]+\s*mmHg?)",
    "heart_rate":       r"(?:HR|Heart\s+Rate|Pulse)[:\s]+(\d+\s*(?:bpm|/min)?)",
    "temperature":      r"(?:Temp(?:erature)?)[:\s]+([\d.]+\s*[°°]?[FC]?)",
    "oxygen_saturation":r"(?:SpO2|O2\s+Sat(?:uration)?)[:\s]+(\d+\s*%?)",
    "respiratory_rate": r"(?:RR|Resp(?:iratory)?\s+Rate)[:\s]+(\d+\s*(?:breaths?/min)?)",
    "weight":           r"(?:Weight|Wt\.?)[:\s]+([\d.]+\s*(?:kg|lbs?))",
    "height":           r"(?:Height|Ht\.?)[:\s]+([\d.]+\s*(?:cm|ft|m))",
    "bmi":              r"BMI[:\s]+([\d.]+)",
}

LAB_PATTERN = re.compile(
    r"([A-Za-z][\w\s\-()]+?)\s+"
    r"([\d.]+)\s*"
    r"([A-Za-z/%μ]+(?:/[A-Za-z]+)?)?\s*"
    r"(?:\(?([\d.]+-[\d.]+)\)?)?\s*"
    r"(Normal|High|Low|Critical|Abnormal|H|L|N)?",
    re.MULTILINE
)

MEDICATION_PATTERN = re.compile(
    r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+"
    r"([\d.]+\s*(?:mg|mcg|g|ml|IU|units?))\s*"
    r"(?:(once|twice|thrice|\d+\s*times?)\s*(?:daily|a\s+day|per\s+day))?\s*"
    r"(?:(oral|IV|IM|SC|sublingual|topical))?\s*"
    r"(?:for\s+([\d]+\s*(?:days?|weeks?|months?)))?",
    re.IGNORECASE
)

DIAGNOSIS_PATTERN = re.compile(
    r"(?:Diagnosis|DX|Impression)[:\s]+([^\n]+)",
    re.IGNORECASE
)

ICD_PATTERN = re.compile(r"\b([A-Z]\d{2}(?:\.\d+)?)\b")

RECOMMENDATION_KEYWORDS = ["recommend", "advised", "should", "must", "follow", "avoid",
                            "continue", "discontinue", "monitor", "schedule"]


def _extract_field(text: str, patterns: List[str]) -> Optional[str]:
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None


def _extract_vitals(text: str) -> VitalSigns:
    vitals = {}
    for field, pat in VITAL_PATTERNS.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            vitals[field] = m.group(1).strip()
    return VitalSigns(**vitals)


def _extract_lab_results(text: str) -> List[LabResult]:
    results = []
    # Look for table-like sections
    lab_section = re.search(
        r"(?:Laboratory|Lab|Test)\s+Results?.*?(?=Medications?|Diagnosis|Impression|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    search_text = lab_section.group(0) if lab_section else text

    for m in LAB_PATTERN.finditer(search_text):
        name = m.group(1).strip()
        # Filter out common false-positives
        if len(name) < 3 or name.lower() in {"the", "and", "for", "date", "name"}:
            continue
        results.append(LabResult(
            test_name=name,
            value=m.group(2).strip(),
            unit=m.group(3).strip() if m.group(3) else None,
            reference_range=m.group(4).strip() if m.group(4) else None,
            status=m.group(5).strip() if m.group(5) else None,
        ))
    return results[:20]  # cap at 20


def _extract_medications(text: str) -> List[Medication]:
    meds = []
    med_section = re.search(
        r"(?:Medications?|Prescriptions?|Drugs?)[:\s].*?(?=Diagnosis|Lab|Vital|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    search_text = med_section.group(0) if med_section else text
    for m in MEDICATION_PATTERN.finditer(search_text):
        meds.append(Medication(
            name=m.group(1).strip(),
            dosage=m.group(2).strip() if m.group(2) else None,
            frequency=m.group(3).strip() if m.group(3) else None,
            route=m.group(4).strip() if m.group(4) else None,
            duration=m.group(5).strip() if m.group(5) else None,
        ))
    return meds[:10]


def _extract_diagnosis(text: str) -> Diagnosis:
    primary = None
    secondary = []
    icd_codes = ICD_PATTERN.findall(text)
    for m in DIAGNOSIS_PATTERN.finditer(text):
        val = m.group(1).strip()
        if not primary:
            primary = val
        else:
            secondary.append(val)
    return Diagnosis(primary=primary, secondary=secondary[:5], icd_codes=icd_codes[:10])


def _extract_recommendations(text: str) -> List[str]:
    recs = []
    for line in text.split("\n"):
        if any(kw in line.lower() for kw in RECOMMENDATION_KEYWORDS):
            clean = line.strip().lstrip("•-*").strip()
            if 10 < len(clean) < 300:
                recs.append(clean)
    return recs[:10]


def _determine_document_type(text: str) -> str:
    text_lower = text.lower()
    if "discharge summary" in text_lower:
        return "Discharge Summary"
    if "laboratory" in text_lower or "lab report" in text_lower:
        return "Lab Report"
    if "prescription" in text_lower or "rx" in text_lower:
        return "Prescription"
    if "radiology" in text_lower or "x-ray" in text_lower or "mri" in text_lower:
        return "Radiology Report"
    if "ecg" in text_lower or "electrocardiogram" in text_lower:
        return "ECG Report"
    if "pathology" in text_lower:
        return "Pathology Report"
    return "Medical Document"


# ─── Main Extractor ───────────────────────────────────────────────────────────

class DocumentIntelligenceService:
    """
    Extracts structured medical data from PDFs using PyMuPDF + regex heuristics
    with Pydantic schema validation.
    """

    def extract_from_pdf(self, file_path: str, doc_id: str) -> MedicalDocumentExtraction:
        """Parse a PDF file and return a validated MedicalDocumentExtraction."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        full_text = ""
        pages = 0
        try:
            doc = fitz.open(str(path))
            for page in doc:
                full_text += page.get_text("text") + "\n"
                pages += 1
            doc.close()
        except Exception as e:
            logger.error(f"PyMuPDF error: {e}")
            raise RuntimeError(f"Failed to parse PDF: {e}")

        return self._extract_from_text(full_text, doc_id, pages)

    def extract_from_text(self, text: str, doc_id: str) -> MedicalDocumentExtraction:
        """Extract from raw text (used for testing/mocking)."""
        return self._extract_from_text(text, doc_id, pages=1)

    def _extract_from_text(
        self, text: str, doc_id: str, pages: int
    ) -> MedicalDocumentExtraction:
        fields_extracted = 0
        total_fields = 8  # tracked patient fields

        def get_field(key: str) -> Optional[str]:
            nonlocal fields_extracted
            val = _extract_field(text, PATTERNS[key])
            if val:
                fields_extracted += 1
            return val

        patient_name      = get_field("patient_name")
        patient_id        = get_field("patient_id")
        patient_age       = get_field("patient_age")
        patient_gender    = get_field("patient_gender")
        date_of_report    = get_field("date_of_report")
        attending         = get_field("attending_physician")
        hospital          = get_field("hospital_name")
        department        = get_field("department")
        chief_complaint   = get_field("chief_complaint")
        follow_up         = get_field("follow_up_date")

        vitals      = _extract_vitals(text)
        lab_results = _extract_lab_results(text)
        medications = _extract_medications(text)
        diagnosis   = _extract_diagnosis(text)
        recs        = _extract_recommendations(text)

        # Confidence = weighted score
        confidence = min(1.0, (
            (fields_extracted / total_fields) * 0.4 +
            (min(len(lab_results), 5) / 5) * 0.2 +
            (min(len(medications), 3) / 3) * 0.2 +
            (1.0 if diagnosis.primary else 0.0) * 0.2
        ))

        # Pull clinical notes (first 500 chars of body text)
        clinical_notes = None
        notes_match = re.search(
            r"(?:Clinical\s+Notes?|History|SOAP)[:\s]+(.{50,500})",
            text, re.IGNORECASE | re.DOTALL
        )
        if notes_match:
            clinical_notes = notes_match.group(1).strip()[:500]

        return MedicalDocumentExtraction(
            document_id=doc_id,
            document_type=_determine_document_type(text),
            patient_name=patient_name,
            patient_id=patient_id,
            patient_age=patient_age,
            patient_gender=patient_gender,
            date_of_report=date_of_report,
            attending_physician=attending,
            department=department,
            hospital_name=hospital,
            vital_signs=vitals,
            lab_results=lab_results,
            medications=medications,
            diagnosis=diagnosis,
            chief_complaint=chief_complaint,
            clinical_notes=clinical_notes,
            recommendations=recs,
            follow_up_date=follow_up,
            raw_text_length=len(text),
            pages_processed=pages,
            extraction_confidence=round(confidence, 3),
        )
