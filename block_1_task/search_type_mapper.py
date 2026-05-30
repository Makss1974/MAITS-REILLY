#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - SEARCH TYPE MAPPER (Two-Echelon Strategy Planning)
Stage 1.3: Transforming the domain into a step-by-step strategy from radar to anomalies.
Path: /home/ubuntu/IT-PROJECTS/REILLY/block_1_task/search_type_mapper.py
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SearchTypeMapper:
    """
    Component for two-echelon intelligence mapping.
    Transforms the baseline knowledge domain into a complex network of search tasks.
    """
    def __init__(self, router=None):
        self.router = router

    def map(self, normalized_query: str, domain_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Main method for building the intelligence task plan."""
        logger.info("[Mapper] 🛠️ Calculating two-echelon search strategy...")
        search_tasks = []
        task_counter = 1

        base_queries = [normalized_query]
        
        if "keywords" in domain_meta and domain_meta["keywords"]:
            extended_kw = " ".join(domain_meta["keywords"][:2])
            base_queries.append(f"{normalized_query} {extended_kw}")

        search_tasks.append({
            "task_id": f"T_{task_counter:02d}",
            "search_type": "SEMANTIC",
            "bright_data_tool": "SERP_API",
            "priority": 1,
            "initial_queries": base_queries,
            "meta_instruction": (
                "Echelon 1 (Radar): Gather initial circle of links, mentions, "
                "and sources for baseline analysis."
            )
        })
        task_counter += 1

        target_urls = domain_meta.get("target_urls", [])
        critical_domains = ["SUPPLY_CHAIN_SECURITY", "MARKET_INTELLIGENCE"]
        
        if not target_urls and domain_meta.get("domain") in critical_domains:
            target_urls = ["https://custom-target-node.internal"]

        if target_urls:
            search_tasks.append({
                "task_id": f"T_{task_counter:02d}",
                "search_type": "SPATIAL_INFRA",
                "bright_data_tool": "Web_Scraper_API",
                "priority": 2,
                "initial_queries": target_urls,
                "meta_instruction": (
                    "Echelon 2 (HTML Extraction): Download raw content of direct nodes "
                    "to analyze the delta of changes."
                )
            })
            task_counter += 1

        if domain_meta.get("domain") in critical_domains:
            search_tasks.append({
                "task_id": f"T_{task_counter:02d}",
                "search_type": "TEMPORAL_ANOMALY",
                "bright_data_tool": "Web_Scraper_API",
                "initial_queries": target_urls,
                "priority": 3,
                "meta_instruction": (
                    "Echelon 2 (Temporal Audit): Compare current HTML with archival baseline. "
                    "Identify hidden or removed data blocks."
                )
            })
            task_counter += 1

        clean_text_lower = normalized_query.lower()
        if any(w in clean_text_lower for w in ["factory", "manufacturing", "supply chain"]):
            cross_queries = [
                f"{normalized_query} logistics supply routes tenders",
                f"{normalized_query} raw material procurement metals"
            ]
            search_tasks.append({
                "task_id": f"T_{task_counter:02d}",
                "search_type": "CORRELATION_CROSS",
                "bright_data_tool": "SERP_API",
                "priority": 4,
                "initial_queries": cross_queries,
                "meta_instruction": (
                    "Echelon 2 (Correlation): Expand intelligence perimeter to metal suppliers "
                    "and critical logistic nodes."
                )
            })
            task_counter += 1

        search_tasks.append({
            "task_id": f"T_{task_counter:02d}",
            "search_type": "LINGUISTIC_STRESS",
            "bright_data_tool": "SERP_API",
            "priority": 5,
            "initial_queries": [f"{normalized_query} vacancies urgent deficit overtime"],
            "meta_instruction": (
                "Echelon 2 (Stress Markers): Assess the presence of linguistic crisis markers "
                "in enterprise texts."
            )
        })

        logger.info(
            "[Mapper] ✅ Plan successfully generated. Total tasks: %d", len(search_tasks)
        )
        return search_tasks