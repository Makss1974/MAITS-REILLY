#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - ACTION PROGRAM BUILDER
Stage 1.4: Generation of the final machine manifest and its dynamic reflection.
Path: /home/ubuntu/IT-PROJECTS/REILLY/block_1_task/action_program_builder.py
"""

import logging
import hashlib
import time
from typing import List, Dict, Any
from core_intelligence.router import ReillyLlmRouter
from .models import SearchTask, ActionProgram

logger = logging.getLogger(__name__)

class ActionProgramBuilder:
    """
    Component for the engineering assembly of the action program.
    Packages initial plans and dynamically corrects them based on logical critique.
    """
    def __init__(self, router: ReillyLlmRouter):
        self.router = router

    def build(
        self, validation: Any, classification: Dict[str, Any], search_plan_raw: List[Dict[str, Any]]
    ) -> ActionProgram:
        """Initial assembly of the action program manifest from raw task dictionaries."""
        logger.info("[Builder] 🏗️ Starting initial ActionProgram assembly...")
        
        salt = f"{time.time()}-{validation.normalized_query}"
        query_id = f"REQ_{hashlib.sha1(salt.encode('utf-8')).hexdigest()[:10].upper()}"

        search_tasks = []
        for raw_task in search_plan_raw:
            task = SearchTask(
                task_id=raw_task["task_id"],
                search_type=raw_task["search_type"],
                bright_data_tool=raw_task["bright_data_tool"],
                priority=raw_task["priority"],
                initial_queries=raw_task["initial_queries"],
                meta_instruction=raw_task["meta_instruction"]
            )
            search_tasks.append(task)

        program = ActionProgram(
            query_id=query_id,
            raw_query=validation.normalized_query,
            normalized_query=validation.normalized_query,
            target_domains=[classification.get("domain", "GENERAL")],
            search_tasks=search_tasks,
            plan_robustness="STANDARD"
        )
        
        logger.info(
            "[Builder] Initial manifest %s assembled. Total tasks: %d", 
            query_id, len(search_tasks)
        )
        return program

    def rebuild_with_critic(
        self, current_program: ActionProgram, vulnerabilities: List[Dict[str, str]]
    ) -> ActionProgram:
        """
        REFLECTION LOOP:
        Rebuilds and strengthens the action plan based on vulnerabilities found by the Agent.
        """
        logger.info("[Builder] 🔄 Modifying action plan based on logical critique...")
        
        v_types = [v["type"] for v in vulnerabilities]

        if "BIAS_RISK" in v_types:
            logger.info("[Builder] Optimization: Implementing counter-bias loops.")
            for task in current_program.search_tasks:
                if task.search_type == "SEMANTIC":
                    task.meta_instruction += (
                        " MANDATORY: Include collection of counter-arguments and fact-checking."
                    )
                    extended_queries = []
                    for q in task.initial_queries:
                        extended_queries.append(q)
                        extended_queries.append(f"{q} problems anomaly deficit refutation")
                    task.initial_queries = list(set(extended_queries))

        if "OVER-RELIANCE_ON_SEARCH" in v_types:
            logger.info("[Builder] Optimization: Strengthening search noise filtration.")
            for task in current_program.search_tasks:
                if task.bright_data_tool == "SERP_API":
                    task.meta_instruction += (
                        " STRICT: Ignore news noise. Search only for direct links to tenders, "
                        "PDF reports, and official corporate registries."
                    )

        if "AI_CRITICAL_GAP" in v_types:
            logger.info("[Builder] Optimization: Adding emergency gap-filling task.")
            for task in current_program.search_tasks:
                task.priority += 1
                
            critical_task = SearchTask(
                task_id="T_CRIT",
                search_type="CORRELATION_CROSS",
                bright_data_tool="SERP_API",
                priority=1,
                initial_queries=[f"{current_program.normalized_query} corporate structure owners"],
                meta_instruction=(
                    "CRITICAL TASK: Conduct deep search on primary entity connections, "
                    "hidden holdings, and affiliated corporate structures."
                )
            )
            current_program.search_tasks.append(critical_task)

        current_program.search_tasks = sorted(
            current_program.search_tasks, key=lambda x: x.priority
        )
        current_program.plan_robustness = "HIGH_VERIFIED"
        
        logger.info(
            "[Builder] ✅ Plan successfully hardened. New task count: %d", 
            len(current_program.search_tasks)
        )
        return current_program