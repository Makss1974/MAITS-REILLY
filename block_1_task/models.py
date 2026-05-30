#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | BLOCK 1 - MODELS (Shared Data Models for the Pipeline)
Defines strict data exchange contracts between all system blocks.
Path: /home/ubuntu/IT-PROJECTS/REILLY/block_1_task/models.py
"""

import time
from typing import List, Dict, Any

class SearchTask:
    """
    Model for an individual intelligence gathering task.
    Used by Block 2 to launch specific data collectors.
    """
    def __init__(
        self,
        task_id: str,
        search_type: str,
        bright_data_tool: str,
        priority: int,
        initial_queries: List[str],
        meta_instruction: str
    ):
        self.task_id = task_id
        self.search_type = search_type
        self.bright_data_tool = bright_data_tool
        self.priority = priority
        self.initial_queries = initial_queries
        self.meta_instruction = meta_instruction

    def to_dict(self) -> Dict[str, Any]:
        """Converts the object into a dictionary for JSON packaging."""
        return {
            "task_id": self.task_id,
            "search_type": self.search_type,
            "bright_data_tool": self.bright_data_tool,
            "priority": self.priority,
            "initial_queries": self.initial_queries,
            "meta_instruction": self.meta_instruction
        }


class ActionProgram:
    """
    The main master-manifest passed from Block 1 to Block 2.
    Contains the complete structured action plan and its robustness assessment.
    """
    def __init__(
        self,
        query_id: str,
        raw_query: str,
        normalized_query: str,
        target_domains: List[str],
        search_tasks: List[SearchTask],
        plan_robustness: str = "STANDARD"
    ):
        self.query_id = query_id
        self.raw_query = raw_query
        self.normalized_query = normalized_query
        self.target_domains = target_domains
        self.search_tasks = sorted(search_tasks, key=lambda x: x.priority)
        self.plan_robustness = plan_robustness
        self.created_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Complete conversion of the entire action program into a machine dictionary format."""
        return {
            "query_id": self.query_id,
            "raw_query": self.raw_query,
            "normalized_query": self.normalized_query,
            "target_domains": self.target_domains,
            "plan_robustness": self.plan_robustness,
            "created_at": self.created_at,
            "search_tasks": [task.to_dict() for task in self.search_tasks]
        }


class RejectionReport:
    """
    Emergency pipeline stop model.
    Generated if the incoming request is blocked by the safety security loop.
    """
    def __init__(self, raw_query: str, rejection_reason: str, stage: str = "1.1_VALIDATION"):
        self.raw_query = raw_query
        self.rejection_reason = rejection_reason
        self.stage = stage
        self.timestamp = time.time()
        self.is_rejected = True

    def to_dict(self) -> Dict[str, Any]:
        """Converts the rejection report into a dictionary."""
        return {
            "is_rejected": True,
            "stage": self.stage,
            "raw_query": self.raw_query,
            "rejection_reason": self.rejection_reason,
            "timestamp": self.timestamp
        }