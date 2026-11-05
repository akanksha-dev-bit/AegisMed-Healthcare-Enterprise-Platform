"""
Module 3: Appointment Assistant
LLM function calling to query doctor availability and book mock appointment slots.
Falls back to deterministic mock logic when OpenAI key is not configured.
"""
from __future__ import annotations
import json
import random
import logging
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from enum import Enum

logger = logging.getLogger(__name__)


# ─── Data Models ──────────────────────────────────────────────────────────────

class AppointmentStatus(str, Enum):
    AVAILABLE  = "available"
    BOOKED     = "booked"
    CANCELLED  = "cancelled"
    COMPLETED  = "completed"


class TimeSlot(BaseModel):
    slot_id: str
    doctor_id: str
    doctor_name: str
    specialty: str
    date: str
    time: str
    duration_minutes: int = 30
    status: AppointmentStatus = AppointmentStatus.AVAILABLE
    room: Optional[str] = None


class BookingRequest(BaseModel):
    patient_name: str
    patient_id: Optional[str] = None
    doctor_id: str
    slot_id: str
    reason: Optional[str] = None
    notes: Optional[str] = None


class BookingConfirmation(BaseModel):
    booking_id: str
    patient_name: str
    doctor_name: str
    specialty: str
    date: str
    time: str
    room: Optional[str] = None
    status: AppointmentStatus
    instructions: str
    message: str


class AvailabilityQuery(BaseModel):
    specialty: Optional[str] = None
    doctor_name: Optional[str] = None
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None  # "morning" | "afternoon" | "evening"


class AppointmentResponse(BaseModel):
    intent: str
    message: str
    available_slots: List[TimeSlot] = []
    booking_confirmation: Optional[BookingConfirmation] = None
    follow_up_questions: List[str] = []


# ─── Mock Doctor & Slot Database ──────────────────────────────────────────────

DOCTORS_DB: Dict[str, Dict[str, Any]] = {
    "DR001": {"name": "Dr. Priya Sharma",     "specialty": "Cardiology",         "room": "OPD-201"},
    "DR002": {"name": "Dr. Arjun Mehta",      "specialty": "Neurology",          "room": "OPD-305"},
    "DR003": {"name": "Dr. Sunita Rao",       "specialty": "Orthopedics",        "room": "OPD-102"},
    "DR004": {"name": "Dr. Vikram Patel",     "specialty": "General Medicine",   "room": "OPD-001"},
    "DR005": {"name": "Dr. Kavya Nair",       "specialty": "Pediatrics",         "room": "OPD-203"},
    "DR006": {"name": "Dr. Rohit Gupta",      "specialty": "Dermatology",        "room": "OPD-404"},
    "DR007": {"name": "Dr. Anita Krishnan",   "specialty": "Gynecology",         "room": "OPD-301"},
    "DR008": {"name": "Dr. Sanjay Verma",     "specialty": "Ophthalmology",      "room": "OPD-102"},
    "DR009": {"name": "Dr. Meera Joshi",      "specialty": "Psychiatry",         "room": "OPD-501"},
    "DR010": {"name": "Dr. Rajesh Iyer",      "specialty": "Endocrinology",      "room": "OPD-405"},
}

TIME_SLOTS = {
    "morning":   ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30"],
    "afternoon": ["13:00", "13:30", "14:00", "14:30", "15:00", "15:30"],
    "evening":   ["16:00", "16:30", "17:00", "17:30"],
}

# In-memory booking store
_BOOKINGS: Dict[str, BookingConfirmation] = {}


def _generate_slot_id(doctor_id: str, date_str: str, time_str: str) -> str:
    return f"{doctor_id}-{date_str.replace('-', '')}-{time_str.replace(':', '')}"


def _get_available_slots(
    doctor_id: str,
    target_date: str,
    period: str = "all",
) -> List[TimeSlot]:
    doctor = DOCTORS_DB.get(doctor_id)
    if not doctor:
        return []

    slots = []
    if period == "all":
        all_times = [t for times in TIME_SLOTS.values() for t in times]
    else:
        all_times = TIME_SLOTS.get(period, TIME_SLOTS["morning"])

    # Deterministically mark ~30% of slots as booked
    for time in all_times:
        slot_id = _generate_slot_id(doctor_id, target_date, time)
        is_booked = slot_id in _BOOKINGS or (hash(slot_id) % 10 < 3)
        slots.append(TimeSlot(
            slot_id=slot_id,
            doctor_id=doctor_id,
            doctor_name=doctor["name"],
            specialty=doctor["specialty"],
            date=target_date,
            time=time,
            status=AppointmentStatus.BOOKED if is_booked else AppointmentStatus.AVAILABLE,
            room=doctor["room"],
        ))
    return slots


# ─── LLM Function Definitions ─────────────────────────────────────────────────

APPOINTMENT_FUNCTIONS = [
    {
        "name": "query_doctor_availability",
        "description": (
            "Query available appointment slots for a doctor or specialty on a given date. "
            "Returns a list of open time slots."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "specialty": {
                    "type": "string",
                    "description": "Medical specialty (e.g., 'Cardiology', 'Neurology')",
                },
                "doctor_name": {
                    "type": "string",
                    "description": "Doctor's full name (optional)",
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format. Defaults to today if not provided.",
                },
                "time_preference": {
                    "type": "string",
                    "enum": ["morning", "afternoon", "evening", "all"],
                    "description": "Preferred time of day",
                },
            },
            "required": [],
        },
    },
    {
        "name": "book_appointment",
        "description": "Book a specific appointment slot for a patient.",
        "parameters": {
            "type": "object",
            "properties": {
                "slot_id": {
                    "type": "string",
                    "description": "The slot ID from query_doctor_availability",
                },
                "patient_name": {
                    "type": "string",
                    "description": "Full name of the patient",
                },
                "patient_id": {
                    "type": "string",
                    "description": "Patient ID / MRN (optional)",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the appointment",
                },
            },
            "required": ["slot_id", "patient_name"],
        },
    },
    {
        "name": "cancel_appointment",
        "description": "Cancel an existing appointment booking.",
        "parameters": {
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "string",
                    "description": "The booking confirmation ID",
                },
                "reason": {
                    "type": "string",
                    "description": "Cancellation reason",
                },
            },
            "required": ["booking_id"],
        },
    },
]


# ─── Appointment Service ───────────────────────────────────────────────────────

class AppointmentAssistantService:
    """
    Appointment assistant using LLM function calling (or mock logic).
    Manages doctor availability queries and slot booking.
    """

    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.openai_api_key = openai_api_key
        self.model = model
        self._use_mock = not (openai_api_key and openai_api_key != "your_openai_api_key_here")
        if not self._use_mock:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=openai_api_key)
            except Exception:
                self._use_mock = True

    def chat(self, user_message: str) -> AppointmentResponse:
        """Process a natural-language appointment request."""
        if self._use_mock:
            return self._mock_process(user_message)
        return self._llm_process(user_message)

    # ── Mock Path ──────────────────────────────────────────────────────────────

    def _mock_process(self, message: str) -> AppointmentResponse:
        """Deterministic rule-based appointment assistant (no LLM required)."""
        msg_lower = message.lower()

        # Intent detection
        if any(w in msg_lower for w in ["book", "schedule", "appoint", "reserve"]):
            return self._mock_booking_flow(message)
        elif any(w in msg_lower for w in ["available", "availability", "slot", "when", "free", "open"]):
            return self._mock_availability_query(message)
        elif any(w in msg_lower for w in ["cancel", "reschedule"]):
            return self._mock_cancellation(message)
        else:
            return AppointmentResponse(
                intent="general_inquiry",
                message=(
                    "Hello! I'm 🛡️ AegisMed's Appointment Assistant. I can help you:\n"
                    "- **Check doctor availability** (e.g., 'Show me available Cardiology slots')\n"
                    "- **Book appointments** (e.g., 'Book an appointment with Dr. Sharma tomorrow')\n"
                    "- **Cancel bookings** (e.g., 'Cancel booking BK-12345')\n\n"
                    "What would you like to do?"
                ),
                follow_up_questions=[
                    "Which specialty or doctor are you looking for?",
                    "Do you have a preferred date?",
                    "Morning, afternoon, or evening preference?",
                ],
            )

    def _mock_availability_query(self, message: str) -> AppointmentResponse:
        msg_lower = message.lower()

        # Detect specialty
        specialty = None
        for dr in DOCTORS_DB.values():
            if dr["specialty"].lower() in msg_lower:
                specialty = dr["specialty"]
                break

        # Detect time preference
        period = "all"
        for p in ["morning", "afternoon", "evening"]:
            if p in msg_lower:
                period = p
                break

        # Target date
        target_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        if "today" in msg_lower:
            target_date = date.today().strftime("%Y-%m-%d")
        elif "day after" in msg_lower:
            target_date = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")

        # Collect slots
        all_slots: List[TimeSlot] = []
        for dr_id, dr_info in DOCTORS_DB.items():
            if specialty and dr_info["specialty"] != specialty:
                continue
            slots = _get_available_slots(dr_id, target_date, period)
            all_slots.extend([s for s in slots if s.status == AppointmentStatus.AVAILABLE][:3])

        all_slots = all_slots[:12]  # cap

        filter_desc = f" for {specialty}" if specialty else ""
        msg = (
            f"I found **{len(all_slots)} available slots**{filter_desc} on {target_date}.\n\n"
            "To book a slot, say: *'Book slot [slot_id] for [your name]'*"
        )
        if not all_slots:
            msg = f"No available slots found{filter_desc} on {target_date}. Try a different date or specialty."

        return AppointmentResponse(
            intent="availability_query",
            message=msg,
            available_slots=all_slots,
            follow_up_questions=["Would you like to book one of these slots?"],
        )

    def _mock_booking_flow(self, message: str) -> AppointmentResponse:
        msg_lower = message.lower()

        # Find doctor
        chosen_dr_id = None
        chosen_dr = None
        for dr_id, dr_info in DOCTORS_DB.items():
            if dr_info["name"].lower() in msg_lower or dr_info["specialty"].lower() in msg_lower:
                chosen_dr_id = dr_id
                chosen_dr = dr_info
                break

        if not chosen_dr_id:
            # Default to general medicine
            chosen_dr_id = "DR004"
            chosen_dr = DOCTORS_DB["DR004"]

        # Extract patient name heuristic
        import re
        name_match = re.search(
            r"(?:for|patient|name is?)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
            message
        )
        patient_name = name_match.group(1) if name_match else "Patient"

        target_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        slots = _get_available_slots(chosen_dr_id, target_date, "morning")
        available = [s for s in slots if s.status == AppointmentStatus.AVAILABLE]

        if not available:
            return AppointmentResponse(
                intent="booking",
                message=f"No available slots found for {chosen_dr['name']} on {target_date}. Please try another date.",
                follow_up_questions=["Would you like to check another date?"],
            )

        chosen_slot = available[0]
        booking_id = f"BK-{random.randint(10000, 99999)}"

        confirmation = BookingConfirmation(
            booking_id=booking_id,
            patient_name=patient_name,
            doctor_name=chosen_dr["name"],
            specialty=chosen_dr["specialty"],
            date=chosen_slot.date,
            time=chosen_slot.time,
            room=chosen_slot.room,
            status=AppointmentStatus.BOOKED,
            instructions=(
                "Please arrive 15 minutes early. Bring your photo ID, "
                "insurance card, and any previous medical records."
            ),
            message=f"Your appointment has been confirmed! Booking ID: **{booking_id}**",
        )
        _BOOKINGS[booking_id] = confirmation

        return AppointmentResponse(
            intent="booking_confirmed",
            message=(
                f"✅ Appointment successfully booked!\n\n"
                f"**Doctor:** {chosen_dr['name']} ({chosen_dr['specialty']})\n"
                f"**Date:** {chosen_slot.date} at {chosen_slot.time}\n"
                f"**Room:** {chosen_slot.room}\n"
                f"**Booking ID:** {booking_id}\n\n"
                f"*{confirmation.instructions}*"
            ),
            booking_confirmation=confirmation,
        )

    def _mock_cancellation(self, message: str) -> AppointmentResponse:
        import re
        bk_match = re.search(r"BK-\d+", message, re.IGNORECASE)
        if not bk_match:
            return AppointmentResponse(
                intent="cancellation",
                message="Please provide your booking ID (format: BK-XXXXX) to cancel an appointment.",
                follow_up_questions=["What is your booking ID?"],
            )
        booking_id = bk_match.group(0).upper()
        if booking_id in _BOOKINGS:
            del _BOOKINGS[booking_id]
            return AppointmentResponse(
                intent="cancellation_confirmed",
                message=f"✅ Appointment **{booking_id}** has been successfully cancelled.",
            )
        return AppointmentResponse(
            intent="cancellation_failed",
            message=f"Booking ID **{booking_id}** not found. Please verify and try again.",
        )

    # ── LLM Path (OpenAI Function Calling) ────────────────────────────────────

    def _llm_process(self, message: str) -> AppointmentResponse:
        """Full LLM function-calling flow."""
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are 🛡️ AegisMed's appointment assistant for a hospital. "
                        "Use the provided functions to check doctor availability and book appointments. "
                        "Always confirm details before booking. Be concise and helpful."
                    ),
                },
                {"role": "user", "content": message},
            ]

            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[{"type": "function", "function": f} for f in APPOINTMENT_FUNCTIONS],
                tool_choice="auto",
            )

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls":
                # Execute function calls
                tool_results = []
                available_slots = []
                booking_confirmation = None

                for tc in choice.message.tool_calls:
                    fn_name = tc.function.name
                    fn_args = json.loads(tc.function.arguments)

                    result, slots, conf = self._execute_function(fn_name, fn_args)
                    available_slots.extend(slots)
                    if conf:
                        booking_confirmation = conf
                    tool_results.append({"tool_call_id": tc.id, "result": result})

                # Second LLM pass with tool results
                messages.append(choice.message)
                for tr in tool_results:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tr["tool_call_id"],
                        "content": json.dumps(tr["result"]),
                    })
                final = self._client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                )
                final_text = final.choices[0].message.content

                return AppointmentResponse(
                    intent="function_call",
                    message=final_text or "Done.",
                    available_slots=available_slots,
                    booking_confirmation=booking_confirmation,
                )
            else:
                return AppointmentResponse(
                    intent="general",
                    message=choice.message.content or "How can I help you?",
                )
        except Exception as e:
            logger.error(f"LLM appointment error: {e}")
            return self._mock_process(message)

    def _execute_function(
        self, fn_name: str, fn_args: Dict[str, Any]
    ) -> Tuple[Dict, List[TimeSlot], Optional[BookingConfirmation]]:
        slots = []
        conf = None

        if fn_name == "query_doctor_availability":
            specialty = fn_args.get("specialty")
            target_date = fn_args.get("date", (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
            period = fn_args.get("time_preference", "all")

            for dr_id, dr_info in DOCTORS_DB.items():
                if specialty and dr_info["specialty"].lower() != specialty.lower():
                    continue
                dr_slots = _get_available_slots(dr_id, target_date, period)
                slots.extend([s for s in dr_slots if s.status == AppointmentStatus.AVAILABLE][:4])

            result = {
                "available_slots": [s.model_dump() for s in slots[:10]],
                "count": len(slots[:10]),
            }

        elif fn_name == "book_appointment":
            slot_id = fn_args.get("slot_id", "")
            patient_name = fn_args.get("patient_name", "Patient")
            reason = fn_args.get("reason", "")

            # Parse slot_id: DR001-20241115-0900
            parts = slot_id.split("-")
            dr_id = parts[0] if parts else "DR004"
            dr = DOCTORS_DB.get(dr_id, DOCTORS_DB["DR004"])

            booking_id = f"BK-{random.randint(10000,99999)}"
            conf = BookingConfirmation(
                booking_id=booking_id,
                patient_name=patient_name,
                doctor_name=dr["name"],
                specialty=dr["specialty"],
                date=date.today().strftime("%Y-%m-%d"),
                time="09:00",
                room=dr["room"],
                status=AppointmentStatus.BOOKED,
                instructions="Arrive 15 minutes early with ID and insurance card.",
                message=f"Confirmed! Booking ID: {booking_id}",
            )
            _BOOKINGS[booking_id] = conf
            result = conf.model_dump()

        elif fn_name == "cancel_appointment":
            booking_id = fn_args.get("booking_id", "")
            if booking_id in _BOOKINGS:
                del _BOOKINGS[booking_id]
                result = {"status": "cancelled", "booking_id": booking_id}
            else:
                result = {"status": "not_found", "booking_id": booking_id}
        else:
            result = {"error": f"Unknown function: {fn_name}"}

        return result, slots, conf

    def get_all_doctors(self) -> List[Dict[str, Any]]:
        """Return full doctor roster."""
        return [
            {"doctor_id": did, **info}
            for did, info in DOCTORS_DB.items()
        ]

    def get_bookings(self) -> List[BookingConfirmation]:
        """Return all in-memory bookings."""
        return list(_BOOKINGS.values())
