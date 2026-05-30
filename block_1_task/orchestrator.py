#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - TASK ORCHESTRATOR (Main Pipeline Conductor)
Orchestrates: Validation -> Classification -> Mapping -> Validation Agent -> Reflection.
Path: block_1_task/orchestrator.py
"""

import os
import sys
import json
import logging
import argparse
from typing import Union
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core_intelligence.router import ReillyLlmRouter
from block_1_task.models import ActionProgram, RejectionReport
from block_1_task.task_validator import TaskValidator
from block_1_task.domain_classifier import DomainClassifier
from block_1_task.search_type_mapper import SearchTypeMapper
from block_1_task.action_program_builder import ActionProgramBuilder
from block_1_task.devils_advocate import ValidationAgent

logger = logging.getLogger(__name__)

DEMO_QUERY = (
    "Analyze the 2024 supply chain resilience of EU automotive manufacturing: "
    "factory production capacities, metal procurement tenders, and rail logistics bottlenecks."
)

def run_block_1_task(
    raw_query: str, mode: str = "hackathon"
) -> Union[ActionProgram, RejectionReport]:
    """Main function to launch Block 1. Orchestrates submodules and reflection loop."""
    load_dotenv()
    router = ReillyLlmRouter()

    logger.info("=" * 60)
    logger.info("BLOCK 1 - TASK | Pipeline START [%s]", mode.upper())
    logger.info("=" * 60)
    logger.info("Input Analytical Target: %.120s", raw_query)

    validator = TaskValidator(router)
    validation = validator.validate(raw_query)

    if not validation.is_approved():
        report = RejectionReport(
            raw_query=raw_query,
            rejection_reason=validation.reason or "Unknown validation error",
            stage="1.1_VALIDATION",
        )
        logger.warning("[Orchestrator] Pipeline stopped by Validation Gate at Stage 1.1.")
        return report

    classifier = DomainClassifier(router)
    classification = classifier.classify(validation.normalized_query)

    mapper = SearchTypeMapper(router)
    search_plan_raw = mapper.map(validation.normalized_query, classification)

    builder = ActionProgramBuilder(router)
    action_program = builder.build(validation, classification, search_plan_raw)

    advocate = ValidationAgent(router)
    vulnerabilities = advocate.audit_plan(validation.normalized_query, action_program)

    if vulnerabilities:
        logger.warning(
            "[Orchestrator] ⚠️ Found %d gaps. Launching optimization cycle...", len(vulnerabilities)
        )
        action_program = builder.rebuild_with_critic(
            current_program=action_program,
            vulnerabilities=vulnerabilities
        )
    else:
        logger.info("[Orchestrator] ✅ Initial plan deemed robust on the first pass.")

    logger.info("=" * 60)
    logger.info("BLOCK 1 - TASK | Pipeline COMPLETE ✅")
    logger.info("Passing ActionProgram %s -> BLOCK 2 (DATA COLLECTION)", action_program.query_id)
    logger.info("=" * 60)

    return action_program

def main() -> None:
    """Entry point for standalone CLI execution and testing of Block 1."""
    parser = argparse.ArgumentParser(description="OSINT-REILLY | BLOCK 1 - TASK Pipeline")
    parser.add_argument("query", nargs="?", default=DEMO_QUERY, help="Research query")
    parser.add_argument(
        "--mode",
        choices=["hackathon", "full-tank", "private"],
        default="hackathon",
        help="System launch profile"
    )
    args = parser.parse_args()

    result = run_block_1_task(args.query, args.mode)

    print("\n" + "=" * 60)
    print("BLOCK 1 - TASK | ENGINE OUTPUT")
    print("=" * 60)

    output_dict = result.to_dict()
    output_json = json.dumps(output_dict, ensure_ascii=False, indent=2)
    print(output_json)

    if args.mode == "full-tank":
        output_path = os.path.join(ROOT_DIR, "state", "block1_history.lsonl")
    elif args.mode == "private":
        output_path = os.path.join(ROOT_DIR, "state", "reports", "private", "block1_output.json")
    else:
        # Hackathon mode: save directly to an 'outputs' folder within the project root
        output_path = os.path.join(ROOT_DIR, "outputs", "block1_task_output.json")

    # Safely create all necessary directories if they don't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if args.mode == "full-tank":
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(output_dict, ensure_ascii=False) + "\n")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_json)
        
    logger.info("Workshop results successfully recorded in the loop: %s", output_path)

if __name__ == "__main__":
    main()