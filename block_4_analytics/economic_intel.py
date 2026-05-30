#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 4 - ECONOMIC INTEL (Merged General & Economic Logic)
Path: block_4_analytics/economic_intel.py
Line Length Limit: 100 characters

Contains Market Indicators, Bottleneck Assessment, and Capital Anomaly detection.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EconomicIntelFamily:
    """Family of economic, supply chain, and statistical analysis methods."""

    def __init__(self):
        logger.info("[Economic Intel] 🏭 Activated economic and logistics analysis loop.")

    def analyze_market_indicators(self, raw_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes signals against predefined market and supply chain indicators."""
        full_text = " ".join(
            [f"{s.get('title', '')} {s.get('text_snippet', '')}".lower() for s in raw_signals]
        )
        
        score = 0.0
        detected = []
        
        indicators = {
            "SUPPLY_DEFICIT": ["vacancy", "shortage", "urgently", "hiring"],
            "LOGISTICS_DELAY": ["railway", "route", "wagon", "delayed", "platform"],
            "PROCUREMENT_SPIKE": ["tender", "procurement", "metal", "budget", "cost"]
        }
        
        for ind_name, keywords in indicators.items():
            if any(kw in full_text for kw in keywords):
                score += 0.35
                detected.append(ind_name)
                
        return {
            "market_indicator_score": round(min(1.0, score), 2),
            "active_market_markers": detected
        }

    def evaluate_bottlenecks(self, raw_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Looks for resource deficits, labor shortages, and infrastructure overload."""
        detected_bottlenecks = []
        full_text = " ".join(
            [f"{s.get('title', '')} {s.get('text_snippet', '')}".lower() for s in raw_signals]
        )

        if any(w in full_text for w in ["deficit", "vacancy", "seeking engineer"]):
            detected_bottlenecks.append("HUMAN_RESOURCE_CONSTRAINT")
        if any(w in full_text for w in ["delay", "wagon", "freight"]):
            detected_bottlenecks.append("LOGISTICS_BOTTLENECK")
            
        return {
            "detected_bottlenecks": detected_bottlenecks,
            "supply_chain_risk_score": 0.8 if detected_bottlenecks else 0.2
        }
        
    def detect_capital_anomaly(self, raw_signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detects financial vs. physical reality anomalies."""
        full_text = " ".join(
            [f"{s.get('title', '')} {s.get('text_snippet', '')}".lower() for s in raw_signals]
        )
        
        has_high_finance = "billion" in full_text or "record budget" in full_text
        has_low_physics = "delay" in full_text or "deficit" in full_text
        
        inversion_anomaly = has_high_finance and has_low_physics
        risk_score = 0.85 if inversion_anomaly else (0.35 if has_high_finance else 0.1)

        return {
            "capital_inversion_anomaly_found": inversion_anomaly,
            "financial_vs_physical_risk_score": risk_score,
            "verdict": "STRUCTURAL_BUBBLE_RISK" if inversion_anomaly else "NORMAL"
        }