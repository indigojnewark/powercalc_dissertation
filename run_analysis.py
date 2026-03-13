"""
run_analysis.py
---------------
End-to-end post-hoc power analysis pipeline for:

  "Effects of systemic bacterial infection on the hippocampal proteome
   in a mouse model of Alzheimer's disease"

  BSc Neuroscience Dissertation, University of Nottingham, 2026
  Author: Indigo Newark

Usage:
    python run_analysis.py
"""

import os
import numpy as np

from src.data_loader import inspect_workbook, load_sheet, get_lfq_values
from src.effect_size import compute_effect_sizes, summarise_effect_sizes
from src.power_analysis import print_power_report

# --- Configuration ---
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "IJN_Data.xlsx")
PROVISION_FILE = os.path.join(DATA_DIR, "IJN_Provision.xlsx")

# Key comparison: AD vs AD+Infection
SHEET = "AD-ADinfec"
GROUP_A_COLS = [0, 1, 2]    # LFQ intensity AD1-3
GROUP_B_COLS = [3, 4, 5]    # LFQ intensity ADInfec1-3

# Actual experimental group sizes
ACTUAL_NS = [5, 6]


def main():
    # --- Step 1: Inspect data files ---
    print("Inspecting data files...\n")
    inspect_workbook(DATA_FILE)
    if os.path.exists(PROVISION_FILE):
        inspect_workbook(PROVISION_FILE)

    # --- Step 2: Load LFQ data for key comparison ---
    print(f"\nLoading sheet '{SHEET}' from {DATA_FILE}...")
    rows = load_sheet(DATA_FILE, SHEET)
    print(f"Total rows (including header): {len(rows)}")

    protein_data = get_lfq_values(rows, GROUP_A_COLS, GROUP_B_COLS, min_valid=2)
    print(f"Proteins with >=2 valid values in both groups: {len(protein_data)}")

    # --- Step 3: Compute Cohen's d ---
    print("\nComputing Cohen's d across proteins (log2 LFQ)...")
    ds = compute_effect_sizes(protein_data)
    summarise_effect_sizes(ds)

    median_d = float(np.median(ds))
    p25_d = float(np.percentile(ds, 25))

    # --- Step 4: Power analysis ---
    effect_sizes = {
        "Median d": median_d,
        "25th pctile d (conservative)": p25_d,
        "Conservative d=0.40": 0.40,
        "Interaction (half median)": median_d / 2,
        "Interaction (half 25th pctile)": p25_d / 2,
    }

    print()
    print_power_report(effect_sizes, actual_ns=ACTUAL_NS)


if __name__ == "__main__":
    main()
