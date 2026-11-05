"""
MongoDB Async Database Connection using Motor.
Provides fallback error handling if MongoDB is offline.
"""
from __future__ import annotations
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.config import settings

logger = logging.getLogger(__name__)

class MongoDBManager:
    """Async MongoDB manager with graceful offline fallback handling."""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.is_connected: bool = False

    async def connect(self) -> bool:
        """Attempt to connect and ping MongoDB with a short timeout."""
        try:
            self.client = AsyncIOMotorClient(
                settings.mongodb_uri,
                serverSelectionTimeoutMS=2000,
                connectTimeoutMS=2000,
            )
            # Ping database to verify connection
            await self.client.admin.command("ping")
            self.db = self.client[settings.mongodb_db_name]
            self.is_connected = True
            logger.info(f"✅ Connected to MongoDB ({settings.mongodb_uri}/{settings.mongodb_db_name})")
            return True
        except Exception as e:
            self.is_connected = False
            logger.warning(
                f"⚠️ MongoDB connection failed ({settings.mongodb_uri}): {e}. "
                "Operating in in-memory / fallback mode."
            )
            return False

    async def disconnect(self):
        """Close MongoDB connection gracefully."""
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("MongoDB connection closed.")

    # ── Collections & Helpers ──────────────────────────────────────────────────

    def get_collection(self, collection_name: str):
        if self.is_connected and self.db is not None:
            return self.db[collection_name]
        return None

    # ── Appointments ──────────────────────────────────────────────────────────

    async def save_booking(self, booking_data: Dict[str, Any]) -> bool:
        """Store or update an appointment booking in MongoDB."""
        if not self.is_connected:
            return False
        try:
            doc = {**booking_data, "updated_at": datetime.utcnow().isoformat()}
            await self.db.appointments.update_one(
                {"booking_id": booking_data.get("booking_id")},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.utcnow().isoformat()}},
                upsert=True,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to persist booking to MongoDB: {e}")
            return False

    async def get_bookings(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve bookings from MongoDB."""
        if not self.is_connected:
            return []
        try:
            cursor = self.db.appointments.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Failed to fetch bookings from MongoDB: {e}")
            return []

    async def update_booking_status(self, booking_id: str, status: str) -> bool:
        """Update booking status (e.g. cancelled) in MongoDB."""
        if not self.is_connected:
            return False
        try:
            result = await self.db.appointments.update_one(
                {"booking_id": booking_id},
                {"$set": {"status": status, "updated_at": datetime.utcnow().isoformat()}},
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update booking status in MongoDB: {e}")
            return False

    # ── Document Extractions ──────────────────────────────────────────────────

    async def save_document_extraction(self, extraction_data: Dict[str, Any]) -> bool:
        """Store document extraction log in MongoDB."""
        if not self.is_connected:
            return False
        try:
            doc = {
                **extraction_data,
                "created_at": datetime.utcnow().isoformat(),
            }
            await self.db.document_extractions.update_one(
                {"document_id": extraction_data.get("document_id")},
                {"$set": doc},
                upsert=True,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to persist document extraction to MongoDB: {e}")
            return False

    async def get_document_extractions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent document extractions from MongoDB."""
        if not self.is_connected:
            return []
        try:
            cursor = self.db.document_extractions.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Failed to fetch document extractions from MongoDB: {e}")
            return []

    # ── Evaluation Results ────────────────────────────────────────────────────

    async def save_evaluation_result(self, eval_data: Dict[str, Any]) -> bool:
        """Store single evaluation result in MongoDB."""
        if not self.is_connected:
            return False
        try:
            doc = {
                **eval_data,
                "created_at": datetime.utcnow().isoformat(),
            }
            await self.db.evaluation_results.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to persist evaluation result to MongoDB: {e}")
            return False

    async def save_batch_evaluation(self, batch_data: Dict[str, Any]) -> bool:
        """Store batch evaluation report in MongoDB."""
        if not self.is_connected:
            return False
        try:
            doc = {
                **batch_data,
                "created_at": datetime.utcnow().isoformat(),
            }
            await self.db.batch_evaluations.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to persist batch evaluation to MongoDB: {e}")
            return False

    async def get_evaluation_results(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent evaluation results from MongoDB."""
        if not self.is_connected:
            return []
        try:
            cursor = self.db.evaluation_results.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Failed to fetch evaluation results from MongoDB: {e}")
            return []


db_manager = MongoDBManager()

