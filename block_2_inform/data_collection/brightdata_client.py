#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 2 - BrightData Gateway
Path: block_2_inform/data_collection/brightdata_client.py
"""

import os
import time
import random
import logging
from typing import Optional, List, Dict, Any
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

SERP_API_ENDPOINT = "https://api.brightdata.com/serp"
BRIGHTDATA_PROXY_HOST = "brd.superproxy.io"
BRIGHTDATA_PROXY_PORT = 22225

SERP_TIMEOUT_SEC = 30
PROXY_TIMEOUT_SEC = 45
MAX_RETRIES = 3
RETRY_BASE_WAIT = 2.0
HUMAN_PAUSE_MIN = 1.5
HUMAN_PAUSE_MAX = 4.5

class BrightDataClient:
    """Client for external data extraction (SERP and HTML via Proxy)."""
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv("BRIGHTDATA_API_TOKEN", "mock_token_if_missing")
        self.zone_username = os.getenv("BRIGHTDATA_ZONE_USER", "mock_user")
        self.zone_password = os.getenv("BRIGHTDATA_ZONE_PASS", "mock_pass")
        
    def fetch_serp(self, queries: List[str], country: str = "us", language: str = "en") -> List:
        """Fetches SERP data for a list of queries with human-like delays."""
        logger.info("[BrightData] 🌐 Calling SERP API for %d queries...", len(queries))
        results = []
        for q in queries:
            # Placeholder for production API call during Lite MVP demo
            time.sleep(random.uniform(HUMAN_PAUSE_MIN, HUMAN_PAUSE_MAX))
            results.append({
                "status": "SUCCESS", 
                "query": q, 
                "results": [{"title": "Sample OSINT Fact", "link": "http://example.com"}]
            })
        return results

    def fetch_html_via_proxy(self, url: str, zone: str = "residential", country: str = "US") -> str:
        """Fetches raw HTML via BrightData proxy network."""
        logger.info("[BrightData] 🕸️ Fetching HTML via Proxy for: %s", url)
        # Dummy HTML fallback for Hackathon demo mode
        return "<html><body>Sample Supply Chain Data for Demo</body></html>"