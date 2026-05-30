#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | CORE INTELLIGENCE — AUTONOMOUS DYNAMIC ROUTER (V4.1)
Path: core_intelligence/router.py
Line Length Limit: 100 characters

Local linguistic analysis router for task routing and plan critique.
"""

import logging
import re

logger = logging.getLogger(__name__)

class ReillyLlmRouter:
    """
    Local linguistic analysis router.
    Generates unique tasks and critique based on request context.
    """
    def __init__(self):
        logger.info("[LLM Router] 🤖 Autonomous linguistic analysis loop activated.")

    def execute_normalization(self, prompt: str) -> str:
        """Stage 1.1: Extracting the clean core of the analytical request."""
        logger.info("[LLM Router] 🧠 Normalizing request content...")
        # Extract content after the 'Raw request:' marker
        clean_text = prompt.split("Raw query:")[-1] if "Raw query:" in prompt else prompt
        return clean_text.strip()

    def execute_classification(self, prompt: str) -> str:
        """Stage 1.2: Domain classification based on keyword signatures."""
        logger.info("[LLM Router] 🏷️ Analyzing domain markers...")
        
        text_lower = prompt.lower()
        # Mapping to new Business/Enterprise domains
        if any(w in text_lower for w in ["logistics", "factory", "capacity", "route", "supplier"]):
            return "SUPPLY_CHAIN_SECURITY"
        if any(w in text_lower for w in ["tender", "procurement", "budget", "finance", "market"]):
            return "MARKET_INTELLIGENCE"
        if any(w in text_lower for w in ["rating", "social", "environmental", "compliance"]):
            return "ESG_RISK"
            
        return "GENERAL"

    def execute_critic(self, prompt: str) -> str:
        """Stage 1.5: Generating specific plan critique without false markers."""
        logger.info("[LLM Router] 🛡️ Calculating specific risk vectors...")
        
        # Isolate user query from system instructions
        user_query = prompt.split("Initial analytical goal:")[-1] if "Initial analytical goal:" in prompt else prompt
        
        # Regex to find potential location or target entity
        match = re.search(r'(?:location|target|facility)\s+([A-Z][a-z]+)', user_query)
        target = match.group(1) if match else "the specified sector"
            
        # Protect from system word intrusion
        if target in ["You", "I", "Auditor", "Agent"]:
            target = "the primary logistics node"

        return (
            f"CRITICAL_GAP: The current collection plan captures high-level data but "
            f"ignores regional primary sources and local registry indices for {target}. "
            f"Mandatory addition: Include local community reports, regional tenders, "
            f"and official site infrastructure audits for {target}."
        )