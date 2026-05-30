#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 5 - REPORT BUILDER (Final Output Generator)
Path: block_5_report/report_builder.py
Line Length Limit: 100 characters

Generates final enterprise intelligence reports in JSON, Markdown, and HTML formats.
Features Trust Gate Status and Graph RAG AI Insights.
"""

import json
import logging
import os
import sys
import time
from enum import Enum
from typing import Dict, Any, Optional

# Dynamic path resolution to project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from block_4_analytics.analytics_engine import AnalyticsResult

logger = logging.getLogger(__name__)

class ReportFormat(str, Enum):
    """Supported output formats for the final report."""
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"

class ClassificationLevel(str, Enum):
    """Enterprise-grade security classifications."""
    PUBLIC = "PUBLIC // UNCLASSIFIED"
    INTERNAL = "RESTRICTED // ENTERPRISE INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL // PROPRIETARY INTELLIGENCE"

class GeneratedReport:
    """Object holding the final report in multiple presentation formats."""
    def __init__(self, report_id: str, query_id: str):
        self.report_id = report_id
        self.query_id = query_id
        self.timestamp = time.time()
        self.classification = ""
        self.raw_data: Dict[str, Any] = {}
        self.markdown_body: str = ""
        self.html_body: str = ""

class ReportBuilder:
    """Constructs analytical reports with Trust Gate and AI Insights."""
    def __init__(self, default_output_dir: Optional[str] = None):
        # Default save location uses dynamic ROOT_DIR to avoid hardcoded paths
        self.default_output_dir = default_output_dir or os.path.join(
            ROOT_DIR, "outputs", "reports"
        )
        os.makedirs(self.default_output_dir, exist_ok=True)
        logger.info("[Report Builder] 🖨️ Enterprise Reporting Module initialized.")

    def build(
        self, 
        analytics_result: AnalyticsResult, 
        classification: ClassificationLevel = ClassificationLevel.INTERNAL
    ) -> GeneratedReport:
        """Compiles the analytical results into Markdown and HTML structures."""
        logger.info(
            "[Report Builder] 📝 Compiling multi-format report: %s", analytics_result.query_id
        )
        
        report_id = f"RPT_{int(time.time())}_{analytics_result.query_id[-6:]}"
        report = GeneratedReport(report_id, analytics_result.query_id)
        report.classification = classification.value
        report.raw_data = analytics_result.to_dict()

        # Extract Key Metrics for Headers
        trust_gate = analytics_result.summary_metrics.get("trust_gate_status", "UNKNOWN")
        confidence_pct = int(analytics_result.overall_confidence * 100)
        
        bottlenecks = analytics_result.bottlenecks
        bottleneck_str = ", ".join(bottlenecks) if bottlenecks else "None detected"
        advisory = analytics_result.advisory_notes
        forecast = analytics_result.forecast_summary
        verified_facts = analytics_result.summary_metrics.get('direct_facts_detected', 0)

        # ---------------------------------------------------------
        # Build 1: Markdown Version (For GitHub / README displays)
        # ---------------------------------------------------------
        md = f"# ENTERPRISE INTELLIGENCE REPORT\n"
        md += f"**ID:** {report_id} | **Target:** {analytics_result.query_id}\n"
        md += f"**Classification:** {classification.value}\n"
        md += f"---\n\n"
        
        md += f"## 🛡️ Trust Gate Verification Status\n"
        md += f"- **Status:** `{trust_gate}`\n"
        md += f"- **Overall Confidence:** {confidence_pct}%\n"
        md += f"- **Verified Facts:** {verified_facts}\n\n"

        md += f"## 🧠 Graph RAG AI Insights\n"
        md += f"- **Primary Bottlenecks:** {bottleneck_str}\n"
        md += f"- **Risk Forecast:** {forecast}\n"
        md += f"- **Advisory Notes:** {advisory}\n\n"

        md += f"## 📊 Analytical Layers Breakdown\n"
        for layer_name, layer_data in analytics_result.layers_output.items():
            md += f"### {layer_name}\n```json\n"
            md += json.dumps(layer_data, indent=2, ensure_ascii=False)
            md += "\n```\n\n"

        report.markdown_body = md

        # ---------------------------------------------------------
        # Build 2: HTML Version (For UI Demo to Judges)
        # ---------------------------------------------------------
        color_trust = "green" if trust_gate == "GROUNDED" else "red"
        html = f"""
        <html>
        <head>
            <title>Intelligence Report | {report_id}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Verdana, sans-serif; margin: 40px; }}
                .header {{ border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 20px; }}
                .trust-gate {{ border-left: 5px solid {color_trust}; padding: 15px; background: #f8f9fa; }}
                .ai-insights {{ border-left: 5px solid #6c757d; padding: 15px; background: #e9ecef; margin-top: 20px; }}
                .layer-box {{ background-color: #f1f3f5; padding: 10px; border-radius: 5px; margin-bottom: 10px; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🏢 Enterprise Intelligence Report</h2>
                <p><strong>Target ID:</strong> {analytics_result.query_id} | 
                   <strong>Classification:</strong> {classification.value}</p>
            </div>
            
            <div class="trust-gate">
                <h3>🛡️ Trust Gate Verification Status: {trust_gate}</h3>
                <p><strong>System Confidence Level:</strong> {confidence_pct}%</p>
                <p><strong>Direct Facts Processed:</strong> {verified_facts}</p>
            </div>

            <div class="ai-insights">
                <h3>🧠 Graph RAG AI Insights</h3>
                <p><strong>Identified Bottlenecks:</strong> {bottleneck_str}</p>
                <p><strong>Risk Forecast:</strong> {forecast}</p>
                <p><strong>Strategic Advisory:</strong> {advisory}</p>
            </div>

            <h3>📊 Analytical Layers</h3>
        """
        
        for layer_name, layer_data in analytics_result.layers_output.items():
            html += f"<div class='layer-box'><h4>{layer_name}</h4>"
            html += f"<pre>{json.dumps(layer_data, indent=2, ensure_ascii=False)}</pre></div>"

        html += "</body></html>"
        report.html_body = html

        logger.info("[Report Builder] ✅ Report %s successfully compiled.", report_id)
        return report

    def save_report_to_disk(
        self, generated_report: GeneratedReport, fmt: ReportFormat, custom_dir: Optional[str] = None
    ) -> str:
        """Saves the requested format to the target output directory."""
        target_dir = custom_dir or self.default_output_dir
        os.makedirs(target_dir, exist_ok=True)
        
        filename = f"report_{generated_report.query_id}"
        path = ""
        
        if fmt == ReportFormat.JSON:
            path = os.path.join(target_dir, f"{filename}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(generated_report.raw_data, f, ensure_ascii=False, indent=2)
        elif fmt == ReportFormat.MARKDOWN:
            path = os.path.join(target_dir, f"{filename}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(generated_report.markdown_body)
        elif fmt == ReportFormat.HTML:
            path = os.path.join(target_dir, f"{filename}.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(generated_report.html_body)
                
        logger.info("[Report Builder] Report saved to disk: %s", path)
        return path