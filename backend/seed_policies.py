"""
🛡️ AegisMed — Hospital Policy Database Seeder
Seeds ChromaDB with sample hospital policy documents.
Run: python backend/seed_policies.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.modules.policy_rag import PolicyRAGService
from backend.config import settings

POLICIES = [
    {
        "source": "Patient Rights & Responsibilities Policy v3.2",
        "section": "Patient Rights",
        "content": """
PATIENT RIGHTS AND RESPONSIBILITIES POLICY

1. PATIENT RIGHTS
Every patient at 🛡️ AegisMed Hospital has the right to:
- Receive compassionate, respectful care regardless of age, gender, race, religion, or disability.
- Be fully informed about their diagnosis, treatment options, and prognosis in language they can understand.
- Participate in decisions about their care, including the right to refuse treatment.
- Privacy and confidentiality of their medical records in accordance with HIPAA regulations.
- Access their medical records within 30 business days of a written request.
- Designate a personal representative or surrogate decision-maker.
- File a complaint or grievance without fear of retaliation.
- Receive emergency care regardless of ability to pay.
- Know the names and roles of all healthcare providers involved in their care.

2. PATIENT RESPONSIBILITIES
Patients are expected to:
- Provide accurate and complete information about their health history.
- Follow the treatment plan recommended by their care team.
- Notify the hospital of any changes in their condition.
- Be respectful of hospital staff, other patients, and visitors.
- Follow hospital rules regarding visiting hours and safety policies.
- Settle financial obligations in a timely manner.
- Inform the team if they do not understand instructions.
        """,
    },
    {
        "source": "Data Privacy & HIPAA Compliance Policy v2.1",
        "section": "Data Protection",
        "content": """
DATA PRIVACY AND HIPAA COMPLIANCE POLICY

1. SCOPE
This policy applies to all employees, contractors, volunteers, and students who handle Protected Health Information (PHI) at 🛡️ AegisMed Hospital.

2. DATA CLASSIFICATION
- Highly Sensitive: Patient identifiers (name, DOB, SSN, MRN), diagnoses, medications, lab results.
- Sensitive: Billing information, insurance data.
- Internal: Non-patient operational data.

3. ELECTRONIC HEALTH RECORDS (EHR) SECURITY
- All EHR data is encrypted at rest using AES-256 and in transit using TLS 1.3.
- Access to patient records is role-based and logged for audit purposes.
- Sessions automatically time out after 15 minutes of inactivity.
- Multi-factor authentication is required for all clinical system logins.

4. BREACH NOTIFICATION
- Any suspected data breach must be reported to the Privacy Officer within 1 hour.
- Affected patients must be notified within 60 days of breach discovery.
- The Department of Health and Human Services must be notified within 60 days.

5. MINIMUM NECESSARY STANDARD
Staff must access only the minimum PHI necessary to perform their job functions. Unauthorized access to patient records is subject to immediate disciplinary action.
        """,
    },
    {
        "source": "ICU Visiting Hours & Family Policy v1.8",
        "section": "Visiting Policy",
        "content": """
ICU VISITING HOURS AND FAMILY POLICY

1. STANDARD VISITING HOURS
Intensive Care Unit (ICU) visiting hours:
- Morning Session: 10:00 AM – 12:00 PM
- Evening Session: 4:00 PM – 6:00 PM
- Special exceptions may be granted at the discretion of the attending physician.

2. VISITOR RESTRICTIONS
- Maximum two (2) visitors per patient at any given time.
- Children under 12 years of age are NOT permitted in the ICU or NICU.
- Visitors showing signs of illness (fever, cough, cold) will be asked to leave.
- Mobile phones must be kept on silent mode; no flash photography.

3. FAMILY CONSULTATION ROOMS
Family waiting areas are located on the 3rd floor (ICU wing). Consultation rooms are available upon request from the charge nurse.

4. NEONATAL ICU (NICU) POLICY
- Parents have 24-hour access to their newborn in NICU.
- Grandparents may visit during standard visiting hours with parental approval.
- Siblings must be over 5 years and healthy.

5. GENERAL WARD VISITING HOURS
- General wards: 9:00 AM – 8:00 PM daily.
- Maximum 4 visitors per patient at a time in general wards.
        """,
    },
    {
        "source": "Medication Safety & Dispensing Policy v4.0",
        "section": "Medication Management",
        "content": """
MEDICATION SAFETY AND DISPENSING POLICY

1. FIVE RIGHTS OF MEDICATION ADMINISTRATION
All nursing staff must verify the five rights before any medication is administered:
1. Right Patient (verify using two patient identifiers: name + date of birth or MRN)
2. Right Drug (confirm medication name, expiry date)
3. Right Dose (confirm dosage calculation)
4. Right Route (oral, IV, IM, SC, topical)
5. Right Time (check scheduled time against MAR)

2. HIGH-ALERT MEDICATIONS
The following medications require double-check by two nurses:
- Insulin (all types)
- Heparin and anticoagulants
- Concentrated electrolytes (KCl > 10 mEq)
- Chemotherapy agents
- Neuromuscular blocking agents

3. MEDICATION ERROR REPORTING
- Any medication dispensing error must be immediately reported to the charge nurse.
- A formal incident report must be submitted within 60 minutes of error discovery.
- The patient must be monitored continuously for adverse reactions.
- The pharmacy department must conduct a root cause analysis within 24 hours.
- Near-misses must also be reported to promote a safety culture.

4. CONTROLLED SUBSTANCES
- All controlled substances are stored in automated dispensing cabinets (ADCs).
- A dual-nurse count is required for all controlled substance transactions.
- Wasting of controlled substances requires two witnesses.
- Discrepancies must be reported immediately to the pharmacy supervisor.
        """,
    },
    {
        "source": "Emergency Response & Code Blue Protocol v5.1",
        "section": "Emergency Procedures",
        "content": """
EMERGENCY RESPONSE AND CODE PROTOCOLS

1. CODE BLUE — CARDIAC/RESPIRATORY ARREST
Activation: Call extension 2222 or pull code blue alarm.
Response Team: Rapid Response Nurse, Intensivist, Cardiologist, Anesthesiologist, Pharmacist.
Steps:
- Initiate CPR immediately (30 compressions : 2 breaths ratio)
- Attach AED or defibrillator
- Establish IV/IO access
- Administer epinephrine 1mg IV every 3-5 minutes
- Consider reversible causes (4 H's and 4 T's)
- Document timeline of events in real time

2. CODE RED — FIRE
- Activate alarm by pull station
- RACE Protocol: Rescue, Alarm, Contain, Evacuate/Extinguish
- Close all fire doors
- Do not use elevators

3. CODE GREY — AGGRESSIVE PATIENT/VISITOR
- Activate by calling extension 2225 or pressing panic button
- Security team and designated clinical staff respond
- Attempt verbal de-escalation first

4. RAPID RESPONSE TEAM (RRT)
Criteria for activation:
- Heart rate < 40 or > 130 bpm
- Respiratory rate < 8 or > 30 breaths/min
- SpO2 < 90% despite oxygen therapy
- Acute change in mental status
- Staff member concerned about patient deterioration
        """,
    },
    {
        "source": "Infection Control & Hand Hygiene Policy v3.5",
        "section": "Infection Prevention",
        "content": """
INFECTION CONTROL AND HAND HYGIENE POLICY

1. HAND HYGIENE — FIVE MOMENTS (WHO Standard)
All healthcare workers must perform hand hygiene:
1. Before touching a patient
2. Before clean/aseptic procedures
3. After body fluid exposure/risk
4. After touching a patient
5. After touching the patient's surroundings

Method: Use alcohol-based hand rub (ABHR) for visibly clean hands. Use soap and water for visibly soiled hands or after caring for C. difficile patients.

2. PERSONAL PROTECTIVE EQUIPMENT (PPE)
Standard Precautions (all patients):
- Gloves: when contact with blood or body fluids expected
- Mask + Eye protection: during aerosol-generating procedures

Droplet Precautions (influenza, COVID-19, RSV):
- Surgical mask within 1 meter of patient
- Private room preferred

Airborne Precautions (TB, Measles, Chickenpox):
- N95 respirator (fit-tested)
- Negative pressure room mandatory

3. CONTACT PRECAUTIONS (MRSA, VRE, C. difficile)
- Gown and gloves required upon entry
- Dedicated equipment (stethoscope, BP cuff) for patient
- Enhanced environmental cleaning with sporicidal agent

4. CENTRAL LINE BUNDLE (CLABSI Prevention)
- Hand hygiene before insertion
- Maximal sterile barrier precautions
- Chlorhexidine skin antisepsis
- Optimal catheter site selection (avoid femoral)
- Daily review of line necessity
        """,
    },
    {
        "source": "Patient Discharge Planning & Readmission Policy v2.3",
        "section": "Discharge Management",
        "content": """
PATIENT DISCHARGE PLANNING AND READMISSION PREVENTION POLICY

1. DISCHARGE PLANNING INITIATION
Discharge planning begins at admission for all inpatients. The multidisciplinary team (MDT) assesses:
- Expected length of stay
- Post-discharge care needs (home care, rehabilitation, skilled nursing)
- Social support and living situation
- Medication management capacity
- Follow-up appointment requirements

2. DISCHARGE CHECKLIST
Before patient leaves, ensure:
- Discharge instructions provided in patient's preferred language.
- Medication reconciliation completed and patient educated on new medications.
- Follow-up appointments scheduled (within 7 days for high-risk patients).
- Emergency contact information provided (hospital hotline: 1800-AEGISMED-1).
- Referrals to community health services made if needed.

3. READMISSION PREVENTION
High-risk patients (LACE score > 10) must:
- Receive a phone call within 48 hours of discharge.
- Have a dedicated care coordinator assigned.
- Be enrolled in the hospital's Remote Patient Monitoring (RPM) program if eligible.

4. UNPLANNED READMISSIONS
Any readmission within 30 days must be reviewed by the quality team. Readmission rate targets: < 8% for cardiac patients, < 10% overall.
        """,
    },
    {
        "source": "Billing & Insurance Verification Policy v1.6",
        "section": "Financial Services",
        "content": """
BILLING AND INSURANCE VERIFICATION POLICY

1. INSURANCE VERIFICATION
All elective procedures require insurance pre-authorization at least 48 hours in advance.
Emergency cases are treated first; insurance verification follows within 24 hours.
Accepted insurance plans: Ayushman Bharat, CGHS, ECHS, ESI, and all major private insurers.

2. BILLING TRANSPARENCY
Patients have the right to receive an itemized bill upon request.
Estimated costs must be provided for planned procedures before admission.
All billing queries should be directed to the Patient Financial Services desk (Ground Floor, Block B).

3. NO-COST SERVICES
The following services are provided free of charge:
- Emergency triage and stabilization
- Pregnancy and childbirth (under government schemes)
- Pediatric vaccinations per national immunization schedule
- Blood pressure and diabetes screening (outpatient)

4. FINANCIAL ASSISTANCE
Patients who are unable to pay may apply for the Hospital Charity Fund.
Applications must be submitted with income proof and BPL card (if applicable).
The finance committee reviews applications within 5 business days.
        """,
    },
]


def seed_policies():
    print("🌱 Seeding hospital policy documents into ChromaDB...")
    service = PolicyRAGService(
        persist_dir=settings.chroma_persist_dir,
        openai_api_key=settings.openai_api_key,
    )

    total_chunks = 0
    for policy in POLICIES:
        chunks = service.index_document(
            content=policy["content"],
            source_document=policy["source"],
            section=policy["section"],
        )
        total_chunks += chunks
        print(f"  ✅ Indexed: {policy['source']} ({chunks} chunks)")

    stats = service.get_stats()
    print(f"\n✨ Seeding complete!")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Documents:    {len(stats['indexed_documents'])}")
    print(f"   Mode:         {stats['embedding_mode']}")
    return service


if __name__ == "__main__":
    seed_policies()
