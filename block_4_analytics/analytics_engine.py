#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 4 - ANALYTICS ENGINE (Hybrid Graph-AI Switcher)
Path: block_4_analytics/analytics_engine.py
Line Length Limit: 100 characters

Orchestrates business intelligence methodologies and evaluates structured knowledge graphs.
"""

import logging
import os
import sys
import time
from enum import Enum
from typing import Dict, Any, List, Optional

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
from core_intelligence.router import ReillyLlmRouter
from block_4_analytics.signal_evaluator import MasterSignalEvaluator
from block_4_analytics.economic_intel import EconomicIntelFamily
from block_4_analytics.social_risk import SocialRiskFamily

logger = logging.getLogger(__name__)

class AnalysisLayer(str, Enum):
    ROOT_CAUSE = "L1_ROOT_CAUSE_ANALYSIS"
    BOTTLENECKS = "L2_SUPPLY_CHAIN_BOTTLENECKS"
    CAPITAL_ANOMALY = "L3_CAPITAL_INVERSION_ANOMALY"
    RISK_FORECAST = "L4_PROBABILISTIC_RISK_FORECAST"

class AnalyticsResult:
    """Final analytical object holding structured enterprise insights."""
    def __init__(self, query_id: str):
        self.query_id = query_id
        self.timestamp = time.time()
        self.layers_output: Dict[str, Any] = {}
        self.summary_metrics: Dict[str, Any] = {}
        self.forecast_summary: str = ""
        self.advisory_notes: str = ""
        self.overall_confidence: float = 0.0
        self.bottlenecks: List[str] = []
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_id": self.query_id,
            "timestamp": self.timestamp,
            "overall_confidence": self.overall_confidence,
            "summary_metrics": self.summary_metrics,
            "forecast_summary": self.forecast_summary,
            "advisory_notes": self.advisory_notes,
            "bottlenecks": self.bottlenecks,
            "layers": self.layers_output
        }

class AnalyticsEngine:
    """Main conductor for the analytical block."""
    def __init__(self, router: Optional[ReillyLlmRouter] = None):
        self.router = router or ReillyLlmRouter()
        self.evaluator = MasterSignalEvaluator()
        
        # Lite MVP Condensed Families
        self.economic_family = EconomicIntelFamily()
        self.social_family = SocialRiskFamily()
        
        logger.info("[Analytics Engine] ⚙️ Enterprise Intelligence Core initialized.")
        
    def run_full_analysis(
        self, query_id: str, raw_signals: List[Dict[str, Any]]
    ) -> AnalyticsResult:
        logger.info("[Analytics Engine] 🔍 Starting deep analysis for %s...", query_id)
        result = AnalyticsResult(query_id)
        
        # Phase 1: Mathematical Signal Passport Evaluation
        total_mass = 0.0
        inverted_mirrors = 0
        direct_facts = 0
        
        for signal in raw_signals:
            passport = self.evaluator.evaluate_signal_passport(signal)
            total_mass += passport["final_weight"]
            if passport["vector"] == "INVERTED_MIRROR":
                inverted_mirrors += 1
            elif passport["vector"] == "DIRECT_FACT":
                direct_facts += 1
                
        logger.info("[Analytics Engine] Signal synthesis complete. Inverted: %d", inverted_mirrors)
        
        # Phase 2: Execute Condensed Enterprise Logic
        res_econ_ind = self.economic_family.analyze_market_indicators(raw_signals)
        res_bottlenecks = self.economic_family.evaluate_bottlenecks(raw_signals)
        res_capital = self.economic_family.detect_capital_anomaly(raw_signals)
        
        res_markov = self.social_family.run_markov_prognosis(inverted_mirrors)
        res_manipulation = self.social_family.detect_market_manipulation(raw_signals)
        
        # Populate Result Layers
        result.bottlenecks = res_bottlenecks.get("detected_bottlenecks", [])
        
        result.layers_output[AnalysisLayer.ROOT_CAUSE.value] = res_econ_ind
        result.layers_output[AnalysisLayer.BOTTLENECKS.value] = res_bottlenecks
        result.layers_output[AnalysisLayer.CAPITAL_ANOMALY.value] = res_capital
        result.layers_output[AnalysisLayer.RISK_FORECAST.value] = res_markov
        
        # Phase 3: Final Metrics & Summaries
        total_processed = len(raw_signals)
        avg_mass = (total_mass / total_processed) if total_processed > 0 else 0.0
        
        result.summary_metrics = {
            "total_signals_verified": total_processed,
            "direct_facts_detected": direct_facts,
            "manipulations_inverted": inverted_mirrors,
            "average_signal_mass": round(avg_mass, 3),
            "trust_gate_status": "GROUNDED" if inverted_mirrors < 2 else "UNSUPPORTED"
        }
        
        prob = int(res_markov['crisis_probability'] * 100)
        result.forecast_summary = (
            f"With a {prob}% probability, the system will enter a "
            f"{res_markov['most_probable_state_6_months']} state in 6 months."
        )
        result.advisory_notes = (
            f"Critical constraints: {', '.join(result.bottlenecks) if result.bottlenecks else 'NONE'}. "
            f"Market manipulation detected: {res_manipulation['detected_manipulation_tactic']}."
        )
        
        # Overall logic confidence score
        result.overall_confidence = round((0.85 if result.bottlenecks else 0.50), 2)
        
        logger.info("=" * 60)
        logger.info("[Analytics Engine] ✅ Enterprise Intelligence Analysis Complete.")
        logger.info("=" * 60)
        return result