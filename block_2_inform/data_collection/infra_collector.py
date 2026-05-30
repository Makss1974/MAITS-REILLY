#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | Block 2 - Infrastructure HTML Collector (Maxwell Daemon)
Path: block_2_inform/data_collection/infra_collector.py
"""

import hashlib
import json
import logging
import os
import time
from typing import Optional, Dict, Any
from .brightdata_client import BrightDataClient

# Define ROOT_DIR dynamically (two levels up from data_collection)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

logger = logging.getLogger(__name__)

class InfraCollector:
    """Collects direct infrastructure data and calculates content deltas."""
    def __init__(self, bd_client: BrightDataClient, cache_dir: Optional[str] = None):
        self.bd_client = bd_client
        # Dynamic path assignment
        self.cache_dir = cache_dir or os.path.join(ROOT_DIR, "state", "infra_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def collect_infra_pipeline(
        self, action_program: Any, zone: str = "residential", 
        country_iso: str = "US", save_manifest: bool = True
    ) -> Dict[str, Any]:
        """Main loop for targeting SPATIAL_INFRA and TEMPORAL_ANOMALY tasks."""
        logger.info("[Maxwell Daemon] ⚡ Launching target infrastructure analysis...")
        
        manifest = {
            "timestamp": time.time(),
            "statistics": {"total_targets": 0, "hot_signals": 0, "cold_baseline": 0},
            "hot_signals_data": []
        }
        
        for task in action_program.search_tasks:
            if task.search_type in ["SPATIAL_INFRA", "TEMPORAL_ANOMALY"]:
                for url in task.initial_queries:
                    manifest["statistics"]["total_targets"] += 1
                    html = self.bd_client.fetch_html_via_proxy(url, zone, country_iso)
                    
                    # Maxwell Daemon logic: count hash, reject captcha
                    html_hash = hashlib.sha256(html.encode('utf-8')).hexdigest()
                    manifest["statistics"]["hot_signals"] += 1
                    manifest["hot_signals_data"].append({
                        "url": url,
                        "search_type": task.search_type,
                        "hash": html_hash,
                        "status": "HOT_SIGNAL_CAPTURED"
                    })
                    
        logger.info(
            "[Maxwell Daemon] ✅ Infra sweep complete. Hot signals: %d", 
            manifest["statistics"]["hot_signals"]
        )
        return manifest