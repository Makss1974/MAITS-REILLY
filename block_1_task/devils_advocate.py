#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - VALIDATION AGENT (Internal Reflection Loop)
Stage 1.5: Stress-testing the action program for logical gaps and collection bias.
Path: /home/ubuntu/IT-PROJECTS/REILLY/block_1_task/devils_advocate.py
"""

import logging
from typing import List, Dict, Any
from core_intelligence.router import ReillyLlmRouter
from .models import ActionProgram

logger = logging.getLogger(__name__)

class ValidationAgent:
    """
    Internal auditor component. Acts as an analytical filter,
    protecting the system from AI hallucinations and superficial planning.
    """
    def __init__(self, router: ReillyLlmRouter):
        self.router = router

    def audit_plan(
        self, query: str, action_program: ActionProgram
    ) -> List[Dict[str, str]]:
        """
        Conducts a comprehensive audit of the generated action program.
        Returns a list of identified vulnerabilities.
        """
        logger.info("[Auditor] 🛡️ Launching forensic analysis of the action program...")
        vulnerabilities = []
        
        tasks = action_program.search_tasks
        
        has_semantic = any(t.search_type == "SEMANTIC" for t in tasks)
        has_spatial = any(t.search_type == "SPATIAL_INFRA" for t in tasks)
        
        if has_spatial and not has_semantic:
            logger.warning("[Auditor] ⚠️ BIAS_RISK detected: Plan ignores semantic balance.")
            vulnerabilities.append({
                "type": "BIAS_RISK",
                "severity": "HIGH",
                "description": (
                    "Plan focuses on raw infrastructure but lacks semantic "
                    "background context gathering."
                )
            })

        serp_count = sum(1 for t in tasks if t.bright_data_tool == "SERP_API")
        if serp_count > 4:
            logger.warning("[Auditor] ⚠️ OVER-RELIANCE detected: Search noise excess.")
            vulnerabilities.append({
                "type": "OVER-RELIANCE_ON_SEARCH",
                "severity": "MEDIUM",
                "description": (
                    f"Too many broad search engine queries ({serp_count}). "
                    "High risk of media spam collection."
                )
            })

        try:
            logger.info("[Auditor] Querying AI router for hidden analytical gaps in the plan...")
            
            tasks_summary = []
            for t in tasks:
                tasks_summary.append(
                    f"- [{t.search_type}] via {t.bright_data_tool}: {t.meta_instruction}"
                )
            tasks_block = "\n".join(tasks_summary)

            critic_prompt = (
                f"You are a Senior Enterprise Risk Analyst. Review this data collection plan.\n"
                f"Initial analytical goal: {query}\n"
                f"Current task plan:\n{tasks_block}\n\n"
                f"Identify the main critical gap in this plan. What is missing?\n"
                f"If it is perfect, output: APPROVED.\n"
                f"If a gap is found, start your response strictly with: CRITICAL_GAP: <description>"
            )

            ai_criticism = self.router.execute_critic(critic_prompt)
            
            if ai_criticism and "CRITICAL_GAP" in ai_criticism:
                gap_description = ai_criticism.replace("CRITICAL_GAP:", "").strip()
                logger.warning("[Auditor] ⚠️ AI found a critical gap: %s", gap_description)
                vulnerabilities.append({
                    "type": "AI_CRITICAL_GAP",
                    "severity": "HIGH",
                    "description": gap_description
                })
            else:
                logger.info("[Auditor] AI loop confirmed the robustness of the plan's logic.")

        except Exception as e:
            logger.error("[Auditor] AI critique error: %s. Using local rules only.", str(e))

        logger.info("[Auditor] 🔍 Audit complete. Vulnerabilities found: %d", len(vulnerabilities))
        return vulnerabilities