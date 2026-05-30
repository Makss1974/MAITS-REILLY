#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | Block 4 - Master Signal Evaluation Matrix
Path: block_4_analytics/signal_evaluator.py
Line Length Limit: 100 characters

Implementation of the 5-Factor Signal Passport Matrix for Enterprise Intelligence.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class MasterSignalEvaluator:
    """Evaluates signals using the 5-factor intelligence matrix."""

    @staticmethod
    def evaluate_signal_passport(report: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesizes 5 factors into a single mathematical signal evaluation model."""
        try:
            # 1. Relevance filter (Gatekeeper)
            relevance = float(report.get("relevance", 0.0))
            if relevance < 0.4:
                return {
                    "final_weight": 0.0,
                    "vector": "DROPPED",
                    "status": "DROPPED_NOT_RELEVANT"
                }

            # 2. Actuality calculation considering static factor (Time Entropy)
            days = max(0.0, float(report.get("days_ago", 0.0)))
            static_factor = max(0.0, min(1.0, float(report.get("static_factor", 1.0))))
            
            actual_multiplier = 1.0 / (1.0 + (days * static_factor))

            # 3. Base importance and content sentiment
            importance = max(0.1, min(1.0, float(report.get("importance", 0.1))))
            sentiment = max(-1.0, min(1.0, float(report.get("sentiment", 0.0))))

            # 4 & 5. Truth assessment via Positioning and Source Authority
            source_bias = max(-1.0, min(1.0, float(report.get("source_positioning", 0.0))))
            source_authority = max(1.0, min(2.0, float(report.get("source_authority", 1.0))))

            # Mathematical synthesis of truth (Dual-loop model)
            if source_bias * sentiment > 0.7:
                truth_index = -1.5 * source_authority  # Inverted logic (overhyped/propaganda)
            else:
                truth_index = 1.0 * source_authority   # Direct factual signal

            final_weight = actual_multiplier * importance * abs(truth_index)

            return {
                "final_weight": round(final_weight, 3),
                "vector": "DIRECT_FACT" if truth_index > 0 else "INVERTED_MIRROR",
                "status": "PROCESSED_SUCCESSFULLY"
            }
        except Exception as e:
            logger.error("[Evaluator] Passport math error: %s", str(e))
            return {"final_weight": 0.1, "vector": "UNKNOWN", "status": "ERROR"}