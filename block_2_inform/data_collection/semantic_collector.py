#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | Block 2 - Semantic Counter-Collector (Red Teaming)
Path: block_2_inform/data_collection/semantic_collector.py
"""

import json
import logging
import os
import time
from typing import Optional, Dict, Any
from .brightdata_client import BrightDataClient

# Define ROOT_DIR dynamically (two levels up from data_collection)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

logger = logging.getLogger(__name__)

class SemanticCollector:
    """Gathers semantic background data and conducts Red Teaming (counter-narratives)."""
    def __init__(self, bd_client: BrightDataClient, router: Any = None, cache_dir: str = None):
        self.bd_client = bd_client
        self.router = router
        # Dynamic path assignment
        self.cache_dir = cache_dir or os.path.join(ROOT_DIR, "state", "semantic_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def collect_semantic_pipeline(
        self, action_program: Any, country: str = "us", 
        language: str = "en", save_cache: bool = True
    ) -> Dict[str, Any]:
        """Executes broad search sweeps based on semantic tasks."""
        logger.info("[Semantic Sweep] 🧠 Launching dual semantic sweep (PRO/CONTRA arguments)...")
        
        result_package = {
            "timestamp": time.time(),
            "semantic_data": []
        }
        
        for task in action_program.search_tasks:
            if task.search_type in ["SEMANTIC", "LINGUISTIC_STRESS", "CORRELATION_CROSS"]:
                serp_raw = self.bd_client.fetch_serp(task.initial_queries, country, language)
                result_package["semantic_data"].append({
                    "search_type": task.search_type,
                    "task_id": task.task_id,
                    "raw_serp": serp_raw
                })
                
        logger.info("[Semantic Sweep] ✅ Semantic collection complete.")
        return result_package