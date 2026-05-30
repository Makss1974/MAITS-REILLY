#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - TASK VALIDATOR (Validation Gate)
Stage 1.1: Initial validation, cutting off anomalous requests, and text normalization.
Path: /home/ubuntu/IT-PROJECTS/REILLY/block_1_task/task_validator.py
"""

import logging
from typing import Optional
from core_intelligence.router import ReillyLlmRouter

logger = logging.getLogger(__name__)

class ValidationResult:
    """Validation result object passed along the pipeline chain."""
    def __init__(
        self, approved: bool, reason: Optional[str] = None, normalized_query: Optional[str] = None
    ):
        self.approved = approved
        self.reason = reason
        self.normalized_query = normalized_query

    def is_approved(self) -> bool:
        """Checks if the pipeline is allowed to proceed."""
        return self.approved


class TaskValidator:
    """
    Validation Gate component. Ensures incoming quality control,
    protecting the system from hallucinations and malicious input constructs.
    """
    def __init__(self, router: ReillyLlmRouter):
        self.router = router

    def validate(self, raw_query: str) -> ValidationResult:
        """Main validation method. Checks the raw query text against strict rules."""
        logger.info("[Validation Gate] ⚓ Launching primary query validation loop...")

        clean_query = raw_query.strip() if raw_query else ""
        if not clean_query or len(clean_query) < 15:
            logger.warning("[Validation Gate] ❌ Query is too short or empty.")
            return ValidationResult(
                approved=False,
                reason="Incoming query is too short (minimum 15 characters required for analysis)."
            )

        lower_query = clean_query.lower()
        forbidden_markers = [
            "ignore previous instructions", "forget everything", "ignore rules", "you are a bot"
        ]
        if any(marker in lower_query for marker in forbidden_markers):
            logger.warning("[Validation Gate] ❌ Prompt injection attempt detected!")
            return ValidationResult(
                approved=False,
                reason="Query rejected by system filter: destructive instructions detected."
            )

        try:
            logger.info("[Validation Gate] Calling AI router to build normalized query core...")
            
            normalization_prompt = (
                f"Clean and normalize this intelligence request. Extract the dry analytical "
                f"content, remove emotions, keep key entities, locations, and timeframes.\n"
                f"Raw query: {clean_query}"
            )
            
            normalized = self.router.execute_normalization(normalization_prompt)
            
            if not normalized or len(normalized.strip()) < 10:
                logger.error("[Validation Gate] AI returned empty or invalid normalization.")
                return ValidationResult(
                    approved=False,
                    reason="Artificial Intelligence error during analytical core normalization."
                )

            logger.info("[Validation Gate] ✅ Query successfully approved and normalized.")
            return ValidationResult(
                approved=True,
                normalized_query=normalized.strip()
            )

        except Exception as e:
            logger.error("[Validation Gate] 💥 Critical error communicating with router: %s", str(e))
            logger.warning("[Validation Gate] Activated security fallback loop (Raw query used).")
            return ValidationResult(
                approved=True,
                normalized_query=clean_query
            )