"""
Module 2: Hospital Policy RAG Search
ChromaDB vector embeddings with strict source document citations.
Falls back to mock embeddings when OpenAI key is not configured.
"""
from __future__ import annotations
import os
import json
import hashlib
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field

import chromadb
from chromadb.utils import embedding_functions
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ─── Data Models ──────────────────────────────────────────────────────────────

class PolicyChunk(BaseModel):
    chunk_id: str
    source_document: str
    section: Optional[str] = None
    page_number: Optional[int] = None
    content: str
    metadata: Dict[str, Any] = {}


class PolicySearchResult(BaseModel):
    answer: str
    citations: List[PolicyChunk]
    query: str
    total_chunks_searched: int
    confidence_score: float


# ─── Policy RAG Service ───────────────────────────────────────────────────────

class PolicyRAGService:
    """
    RAG pipeline over hospital policy documents stored in ChromaDB.
    Provides strict source citations for every answer.
    """

    COLLECTION_NAME = "hospital_policies"

    def __init__(self, persist_dir: str, openai_api_key: Optional[str] = None):
        self.persist_dir = persist_dir
        self.openai_api_key = openai_api_key
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection = None
        self._use_mock = not (openai_api_key and openai_api_key != "your_openai_api_key_here")

    def _get_client(self) -> chromadb.PersistentClient:
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self.persist_dir)
        return self._client

    def _get_collection(self):
        if self._collection is None:
            client = self._get_client()
            if self._use_mock:
                # Use default (deterministic hash-based) embeddings
                ef = embedding_functions.DefaultEmbeddingFunction()
            else:
                ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=self.openai_api_key,
                    model_name="text-embedding-3-small",
                )
            self._collection = client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                embedding_function=ef,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def _chunk_text(
        self, text: str, chunk_size: int = 400, overlap: int = 80
    ) -> List[str]:
        """Split text into overlapping chunks by word count."""
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunks.append(" ".join(words[start:end]))
            start += chunk_size - overlap
        return chunks

    def index_document(
        self,
        content: str,
        source_document: str,
        section: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Index a policy document into ChromaDB. Returns number of chunks added."""
        collection = self._get_collection()
        chunks = self._chunk_text(content)
        added = 0

        for i, chunk in enumerate(chunks):
            chunk_id = hashlib.md5(
                f"{source_document}:{section}:{i}:{chunk[:50]}".encode()
            ).hexdigest()

            meta = {
                "source_document": source_document,
                "section": section or "General",
                "chunk_index": i,
                **(metadata or {}),
            }

            # Add or update
            try:
                collection.upsert(
                    ids=[chunk_id],
                    documents=[chunk],
                    metadatas=[meta],
                )
                added += 1
            except Exception as e:
                logger.warning(f"Failed to upsert chunk {chunk_id}: {e}")

        logger.info(f"Indexed {added} chunks from '{source_document}'")
        return added

    def search(
        self,
        query: str,
        top_k: int = 5,
        source_filter: Optional[str] = None,
    ) -> PolicySearchResult:
        """
        Semantic search over indexed policies with source citations.
        """
        collection = self._get_collection()
        total = collection.count()

        if total == 0:
            return PolicySearchResult(
                answer="No policy documents have been indexed yet. Please seed the policy database first.",
                citations=[],
                query=query,
                total_chunks_searched=0,
                confidence_score=0.0,
            )

        where = {"source_document": {"$eq": source_filter}} if source_filter else None

        results = collection.query(
            query_texts=[query],
            n_results=min(top_k, total),
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        docs      = results["documents"][0]
        metas     = results["metadatas"][0]
        distances = results["distances"][0]

        citations = []
        for doc, meta, dist in zip(docs, metas, distances):
            chunk_id = hashlib.md5(
                f"{meta.get('source_document')}:{meta.get('section')}:{meta.get('chunk_index')}:{doc[:50]}".encode()
            ).hexdigest()
            citations.append(PolicyChunk(
                chunk_id=chunk_id,
                source_document=meta.get("source_document", "Unknown"),
                section=meta.get("section"),
                page_number=meta.get("page_number"),
                content=doc,
                metadata=meta,
            ))

        # Build synthesized answer from top chunks
        answer = self._synthesize_answer(query, citations)
        confidence = max(0.0, 1.0 - (distances[0] if distances else 1.0))

        return PolicySearchResult(
            answer=answer,
            citations=citations,
            query=query,
            total_chunks_searched=total,
            confidence_score=round(confidence, 3),
        )

    def _synthesize_answer(self, query: str, citations: List[PolicyChunk]) -> str:
        """Rule-based answer synthesis from top citation chunks (no LLM required)."""
        if not citations:
            return "No relevant policy information found for this query."

        best = citations[0]
        answer_parts = [
            f"Based on **{best.source_document}**",
            f"(Section: {best.section}):\n\n" if best.section else ":\n\n",
            best.content,
        ]

        if len(citations) > 1:
            answer_parts.append(
                f"\n\n*Additional context from {citations[1].source_document}:* "
                + citations[1].content[:300] + "..."
            )

        answer_parts.append(
            f"\n\n---\n*{len(citations)} source(s) referenced. "
            "See citations below for full context.*"
        )
        return "".join(answer_parts)

    def list_indexed_documents(self) -> List[str]:
        """Return list of unique source documents in the collection."""
        collection = self._get_collection()
        if collection.count() == 0:
            return []
        results = collection.get(include=["metadatas"])
        docs = {m.get("source_document", "Unknown") for m in results["metadatas"]}
        return sorted(docs)

    def get_stats(self) -> Dict[str, Any]:
        """Return collection statistics."""
        collection = self._get_collection()
        return {
            "total_chunks": collection.count(),
            "indexed_documents": self.list_indexed_documents(),
            "collection_name": self.COLLECTION_NAME,
            "embedding_mode": "mock (default)" if self._use_mock else "OpenAI",
        }
