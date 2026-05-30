#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - DOMAIN CLASSIFIER (Ontology Classifier)
Stage 1.2: Identifying target knowledge domains and extracting key markers.
Path: /home/ubuntu/IT-PROJECTS/REILLY/block_1_task/domain_classifier.py
"""

import logging
import re
from typing import Dict, Any

from core_intelligence.router import ReillyLlmRouter

logger = logging.getLogger(__name__)

class DomainClassifier:
    """
    Classification component. Determines the thematic domain of the intelligence request
    to activate appropriate low-level analytical layers.
    """
    def __init__(self, router: ReillyLlmRouter):
        self.router = router
        
        self.signatures = {
            "SUPPLY_CHAIN_SECURITY": [
                "logistics", "factory", "capacity", "route", "supplier", "warehouse", "freight"
            ],
            "MARKET_INTELLIGENCE": [
                "tender", "procurement", "budget", "finance", "cost", "market", "competitor"
            ],
            "ESG_RISK": [
                "protest", "strike", "rating", "social", "environmental", "emission", "compliance"
            ]
        }

    def classify(self, normalized_query: str) -> Dict[str, Any]:
        """Main method for classifying the query by ontological domains."""
        logger.info("[Classifier] 🏷️ Identifying target knowledge domains...")
        
        domain_meta = {
            "domain": "GENERAL",
            "keywords": [],
            "target_urls": [],
            "confidence": 0.5
        }

        urls = re.findall(r'https?://[^\s]+', normalized_query)
        if urls:
            domain_meta["target_urls"] = [url.strip(",.()\"'") for url in urls]
            logger.info("[Classifier] Found direct target URLs: %s", domain_meta["target_urls"])

        try:
            classifier_prompt = (
                f"Determine the knowledge domain for this intelligence request. Options: "
                f"SUPPLY_CHAIN_SECURITY, MARKET_INTELLIGENCE, ESG_RISK, TECH_INNOVATION, PRIVATE.\n"
                f"Request: {normalized_query}\n"
                f"Return the response as a single domain marker word."
            )
            
            ai_domain = self.router.execute_classification(classifier_prompt)
            valid_domains = [
                "SUPPLY_CHAIN_SECURITY", "MARKET_INTELLIGENCE", "ESG_RISK", 
                "TECH_INNOVATION", "PRIVATE"
            ]
            
            if ai_domain and ai_domain.strip() in valid_domains:
                domain_meta["domain"] = ai_domain.strip()
                domain_meta["confidence"] = 0.9
                logger.info("[Classifier] AI determined knowledge domain: %s", domain_meta["domain"])
            else:
                logger.warning("[Classifier] Non-standard AI response. Enabling local signatures.")
                domain_meta = self._run_heuristic_fallback(normalized_query, domain_meta)

        except Exception as e:
            logger.error(
                "[Classifier] AI context analysis error: %s. Fallback to heuristics.", str(e)
            )
            domain_meta = self._run_heuristic_fallback(normalized_query, domain_meta)

        words = normalized_query.lower().split()
        keywords = [
            w.strip(",.()\"'") for w in words 
            if len(w) > 4 and w not in ["analyze", "status", "year", "dynamics"]
        ]
        domain_meta["keywords"] = list(set(keywords))[:5]

        return domain_meta

    def _run_heuristic_fallback(self, text: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        """Local heuristic text analyzer based on root keyword matching."""
        lower_text = text.lower()
        max_matches = 0
        detected_domain = "GENERAL"

        for domain_name, markers in self.signatures.items():
            matches = sum(1 for marker in markers if marker in lower_text)
            if matches > max_matches:
                max_matches = matches
                detected_domain = domain_name

        meta["domain"] = detected_domain
        meta["confidence"] = 0.7
        logger.info(
            "[Classifier Heuristics] Detected fallback domain: %s (matches: %d)", 
            detected_domain, max_matches
        )
        return meta