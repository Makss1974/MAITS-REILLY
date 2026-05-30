#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 3 - ACCESS GUARDIAN (Intelligent Network Routing)
Implements a three-tier Bright Data proxy cascade: Residential ISP -> Mobile 4G -> Web Unlocker.
Path: block_3_access/access_guardian.py
"""

import os
import sys
import logging
import random
import time
from enum import Enum
from typing import Dict, Any, Optional

# Dynamic path assignment for robust imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from block_2_inform.data_collection.brightdata_client import BrightDataClient

logger = logging.getLogger(__name__)

class ProxyPool(str, Enum):
    """Three-tier Bright Data proxy cascade according to MVP specifications."""
    RESIDENTIAL_ISP = "POOL_1_RESIDENTIAL_ISP"
    MOBILE_4G       = "POOL_2_MOBILE_4G"
    WEB_UNLOCKER    = "POOL_3_WEB_UNLOCKER"

class AccessGuardian:
    """
    Network resilience component. Ensures intelligent HTTP routing,
    protecting data collectors from blocks via automated zone rotation.
    """
    def __init__(self, bd_client: Optional[BrightDataClient] = None):
        self.bd_client = bd_client or BrightDataClient()
        self._request_count = 0
        self._blocked_count = 0
        logger.info("[Guardian] 🛡️ Network Resilience Layer initialized.")

    def fetch_secure(self, url: str, country_iso: str = "US") -> str:
        """Executes a secure HTTP fetch using the proxy cascade strategy."""
        self._request_count += 1
        logger.info("[Guardian] 🌐 Initiating secure tunnel sequence for: %s", url)

        pools = [ProxyPool.RESIDENTIAL_ISP, ProxyPool.MOBILE_4G, ProxyPool.WEB_UNLOCKER]

        for attempt, pool in enumerate(pools, start=1):
            try:
                logger.info("[Guardian] Attempt %d/3 - Activating %s", attempt, pool.value)
                
                # Simulated routing zone logic mapping to BrightData client
                zone = "residential" if attempt == 1 else ("mobile" if attempt == 2 else "unlocker")
                
                html_content = self.bd_client.fetch_html_via_proxy(url, zone, country_iso)
                
                if self._is_blocked(html_content):
                    self._blocked_count += 1
                    logger.warning("[Guardian] ⚠️ Block detected on %s. Rotating...", pool.value)
                    time.sleep(2.0 * attempt)
                    continue
                    
                logger.info("[Guardian] ✅ Fetch successful using %s", pool.value)
                return html_content

            except Exception as e:
                logger.error("[Guardian] 💥 Tunnel failure on %s: %s", pool.value, str(e))
                time.sleep(1.5 * attempt)
                continue

        logger.error("[Guardian] 🚨 CRITICAL FAILURE: Entire proxy cascade blocked!")
        return (
            "<html><body>[ERROR_BLOCKED] Target defense systems overwhelmed "
            "the extraction cascade.</body></html>"
        )

    def _is_blocked(self, html: str) -> bool:
        """Checks raw HTML text for parsing counter-measures."""
        if not html or len(html) < 400:
            return True
            
        lower_html = html.lower()
        block_markers = [
            "captcha", "cloudflare", "sucuri", "ddos protection", 
            "access denied", "403 forbidden", "robot", "blocked"
        ]
        return any(marker in lower_html for marker in block_markers)

    def get_guardian_status(self) -> Dict[str, Any]:
        """Returns network resilience statistics for reporting."""
        block_rate = self._blocked_count / max(self._request_count, 1)
        return {
            "total_requests": self._request_count,
            "total_blocks_evaded": self._blocked_count,
            "network_resilience_score": f"{(1.0 - block_rate) * 100:.1f}%",
            "active_cascades": 3
        }