#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | DEMO ENGINE (Fast-Track Presentation Mode)
Path: demo_engine.py
"""

import json
import os
import logging
from block_4_analytics.analytics_engine import AnalyticsEngine
from block_5_report.report_builder import ReportBuilder, ReportFormat

logger = logging.getLogger(__name__)

def run_demo():
    print("[!] OSINT-REILLY | ENTERING DEMO MODE...")
    demo_path = os.path.join("state", "demo_data", "mock_input.json")
    
    if not os.path.exists(demo_path):
        print(f"[!] Error: Mock data not found at {demo_path}")
        return

    # 1. Load mock data
    with open(demo_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    # 2. Skip Block 1 & 2, go straight to Analysis
    engine = AnalyticsEngine()
    result = engine.run_full_analysis("DEMO_REQ_001", mock_data["levels_payload"])

    # 3. Build Report
    builder = ReportBuilder()
    report = builder.build(result)
    
    # 4. Save and show
    path = builder.save_report_to_disk(report, ReportFormat.HTML, "outputs/demo_results")
    print(f"[+] DEMO SUCCESS. Report generated: {path}")
    print("[+] Check the HTML file to see the RAG AI insights!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_demo()