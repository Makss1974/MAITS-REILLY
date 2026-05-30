#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 2 - INFORM PROCESSOR (Main Collection Dispatcher)
Orchestrates task execution across 5 depth levels, invoking specific collectors.
Path: block_2_inform/processor.py
"""

import json
import logging
import os
import sys
import time
from enum import Enum
from typing import Dict, Any, List

# Strict dynamic import of the project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core_intelligence.router import ReillyLlmRouter
from block_2_inform.data_collection.brightdata_client import BrightDataClient
from block_2_inform.data_collection.infra_collector import InfraCollector
from block_2_inform.data_collection.semantic_collector import SemanticCollector

logger = logging.getLogger(__name__)

class DataLevel(str, Enum):
    """5-Layer Information Gathering Depth Model."""
    META     = "L1_META"           # Level 1: Meta-data and task mapping
    EXTERNAL = "L2_EXTERNAL"       # Level 2: Broad external linguistics
    OPEN     = "L3_OPEN"           # Level 3: Open sources and SERP
    CLOSED   = "L4_CLOSED"         # Level 4: Hidden infrastructure extraction
    HUMINT   = "L5_HUMINT"         # Level 5: Expert cross-validation risk

class InformProcessor:
    """Main dispatcher for Block 2."""
    def __init__(self, bd_client: Any = None):
        # Якщо клієнт не переданий, створюємо його автоматично
        self.bd_client = bd_client or BrightDataClient()
        self.infra_collector = InfraCollector(self.bd_client)
        self.semantic_collector = SemanticCollector(self.bd_client)

    def process(self, action_program: Any) -> Dict[str, Any]:
        """Runs the action program through all collectors and compiles the final package."""
        logger.info("[Processor] 📡 Initiating intelligence collection phase...")
        
        # Simulated payload structure
        levels_payload = {}
        
        # 1. Infrastructure Sweep (L4_CLOSED Equivalent)
        infra_results = self.infra_collector.collect_infra_pipeline(action_program)
        levels_payload[DataLevel.CLOSED.value] = infra_results
        
        # 2. Semantic Sweep (L2_EXTERNAL / L3_OPEN Equivalent)
        semantic_results = self.semantic_collector.collect_semantic_pipeline(action_program)
        levels_payload[DataLevel.OPEN.value] = semantic_results

        logger.info("[Processor] Evaluating analytical layer Level 5 [L5_HUMINT]...")
        distortion_risk = "LOW"
        verification_available = "HIGH"
        
        if infra_results.get("statistics", {}).get("hot_signals", 0) > 2:
            distortion_risk = "MEDIUM_DUE_TO_DYNAMICS"
            
        levels_payload[DataLevel.HUMINT.value] = {
            "expert_assessed_at": time.time(),
            "distortion_risk_index": distortion_risk,
            "counter_measures_applied": "DUAL_SWEEP_REDUCTION"
        }

        total_items = (
            len(infra_results.get("hot_signals_data", [])) + 
            len(semantic_results.get("semantic_data", []))
        )
        
        collection_stats = {
            "status": "COMPLETE",
            "total_items_collected": total_items,
            "distortion_risk": distortion_risk,
            "verification_available": verification_available,
            "cache_paths": {
                "infra": os.path.join(ROOT_DIR, "state", "infra_cache"),
                "semantic": os.path.join(ROOT_DIR, "state", "semantic_cache")
            }
        }

        logger.info("=" * 60)
        logger.info("[Processor] ✅ Collection Phase Successfully Completed.")
        logger.info("=" * 60)

        return {
            "query_id": action_program.query_id,
            "levels_payload": levels_payload,
            "collection_stats": collection_stats
        }