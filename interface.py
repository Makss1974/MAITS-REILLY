#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSINT-REILLY | INTERFACE ENGINE
Path: interface.py
Line Length Limit: 100 characters
"""

import sys
import time

def clear_screen():
    print("\033[H\033[J", end="")

def print_banner():
    banner = """
    ========================================================
    OSINT-REILLY | ENTERPRISE INTELLIGENCE ENGINE v4.2
    ========================================================
    """
    print(banner)

def run_interface():
    clear_screen()
    print_banner()
    
    print("System Status: [READY]")
    print("Mode: [HACKATHON_DEMO]")
    print("-" * 55)
    
    # Поле для введення завдання
    query = input("\n[INPUT] Enter intelligence target or analytical query:\n> ")
    
    if not query.strip():
        print("\n[ERROR] Empty input. Pipeline aborted.")
        return

    print("\n[PROCESS] Orchestrating pipeline blocks...")
    
    # Симуляція запуску конвеєра
    stages = ["Tasking", "Collection", "Network Resilience", "Analytics", "Reporting"]
    for stage in stages:
        time.sleep(0.8)
        print(f"  > Executing Block: {stage.ljust(20)} [OK]")

    print("-" * 55)
    print("\n[SUCCESS] Analysis complete.")
    print(f"[OUTPUT] Report saved to: ./outputs/reports/hackathon/")
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    run_interface()