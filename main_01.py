#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | MAIN — CORE ENGINE ORCHESTRATOR
Path: main.py
Line Length Limit: 100 characters

Main pipeline orchestrator for the entire intelligence engine.
"""

import os
import sys
import logging
import time
import argparse

# Dynamic root registration for production-ready imports
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importing Core Intelligence Modules
from core_intelligence.data_storage.storage_manager import StorageManager
from block_1_task.orchestrator import run_block_1_task
from block_2_inform.processor import InformProcessor
from block_4_analytics.analytics_engine import AnalyticsEngine
from block_5_report.report_builder import ReportBuilder, ReportFormat

# Setup logging
LOG_DIR = os.path.join(ROOT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | [REILLY_CORE] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "reilly_core.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

DEFAULT_QUERY = (
    "Analyze the 2024 supply chain resilience of EU automotive manufacturing: "
    "production capacity, metal procurement tenders, and rail logistics bottlenecks."
)

def execute_reilly_engine(query: str, mode: str = "hackathon") -> str:
    """Global execution pipeline for the OSINT-REILLY system."""
    start_time = time.time()
    logger.info("=" * 70)
    logger.info("🛡️  OSINT-REILLY ENGINE CORE v4.2 | PIPELINE START")
    logger.info("=" * 70)

    # Initialize data storage manager
    storage_mgr = StorageManager(base_state_dir=os.path.join(ROOT_DIR, "state"))

    # BLOCK 1: Task Planning
    action_program = run_block_1_task(query, mode=mode)
    if hasattr(action_program, "is_rejected") and action_program.is_rejected:
        logger.warning("[MAIN] ⚠️ Pipeline aborted by Block 1: %s", action_program.rejection_reason)
        return "CONVEYOR_REJECTED"

    # BLOCK 2: Data Collection (Information Processor)
    inform_processor = InformProcessor(bd_client=None) # Client injected if needed
    inform_package = inform_processor.process(action_program)

    # BLOCK 4: Analytics Engine
    analytics_engine = AnalyticsEngine()
    analytics_result = analytics_engine.run_full_analysis(
        action_program.query_id, 
        inform_package["levels_payload"]
    )

    # BLOCK 5: Report Construction
    report_builder = ReportBuilder()
    generated_report = report_builder.build(analytics_result)

    # Save outputs to dynamic paths
    target_dir = os.path.join(ROOT_DIR, "outputs", "reports", mode)
    report_builder.save_report_to_disk(generated_report, ReportFormat.JSON, target_dir)
    report_builder.save_report_to_disk(generated_report, ReportFormat.HTML, target_dir)
    final_md_path = report_builder.save_report_to_disk(generated_report, ReportFormat.MARKDOWN, target_dir)

    elapsed = time.time() - start_time
    logger.info("=" * 70)
    logger.info("✅ OSINT-REILLY ENGINE PIPELINE COMPLETE SUCCESS")
    logger.info("🔑 Query ID: %s | Execution Time: %.2f sec", generated_report.query_id, elapsed)
    logger.info("=" * 70)

    return final_md_path

def main() -> None:
    """CLI Entry point."""
    parser = argparse.ArgumentParser(description="OSINT-REILLY Engine Main Orchestrator")
    parser.add_argument("query", nargs="?", default=DEFAULT_QUERY, help="Research query")
    parser.add_argument("--mode", choices=["hackathon", "full-tank", "private"], default="hackathon")
    args = parser.parse_args()
    execute_reilly_engine(args.query, args.mode)

if __name__ == "__main__":
    main()