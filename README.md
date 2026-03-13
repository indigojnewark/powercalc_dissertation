# Post-Hoc Power Analysis — Undergraduate Neuroscience Dissertation

**Dissertation title:** Effects of systemic bacterial infection on the hippocampal proteome in a mouse model of Alzheimer's disease
**Author:** Indigo Newark
**Institution:** University of Nottingham
**Supervisor:** Dr Graham Sheridan
**Year:** 2026

---

## Overview

This repository contains the Python code used to conduct a post-hoc power analysis for the discussion section of the above dissertation. The analysis quantifies the statistical power of pairwise proteomic comparisons performed on label-free quantification (LFQ) mass spectrometry data from synaptic-enriched hippocampal fractions in a 2x2 factorial mouse model (5xFAD AD genotype x systemic *E. coli* infection).

Four experimental groups were used:
- **Ctrl** — wild-type controls
- **AD** — 5xFAD transgenic mice
- **Infec** — wild-type mice with systemic *E. coli* infection (transurethral UTI model)
- **ADInfec** — 5xFAD mice with systemic infection

The key comparison is between AD and AD+Infection groups (`AD-ADinfec` sheet), using LFQ intensities from MaxQuant output. Effect sizes (Cohen's *d*) were estimated from log2-transformed LFQ values across all proteins with valid quantification in both groups, and power was calculated for a two-sample t-test at alpha = 0.05.

---

## Background

Post-hoc power analysis was conducted to contextualise the study's sample size (n = 5–6 per group). Mice were aged to 10–12 months; systemic infection was induced via transurethral *E. coli* administration at 10 and 11 months, with culling four weeks after the second challenge. Cohen's *d* was estimated across 477 proteins with >= 2 valid values in both comparison groups. The 25th percentile effect size (d = 0.60) was used as a conservative estimate of modest but consistent proteomic shifts; the median (d = 1.19) provides an upper bound.

Key findings:
- At n = 5–6 per group, achieved power for d = 0.60 is ~13–16% — well below the 80% convention
- Achieving 80% power at d = 0.60 would require ~45 animals per group
- For interaction effects (where d ~ 0.30–0.60), 46–176 animals per group would be required — infeasible in preclinical proteomics

These results confirm the dataset is adequately powered for large-effect pairwise differences, but substantially underpowered for small-to-moderate effects and interaction terms, as discussed in Section 4.5 of the dissertation.

---

## Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Place data files
Put `IJN_Data.xlsx` and (optionally) `IJN_Provision.xlsx` in the `data/` directory.

### 3. Run the full analysis
```bash
python run_analysis.py
```

---

## Repository Structure
```
powercalc_dissertation/
├── README.md
├── requirements.txt
├── .gitignore
├── run_analysis.py          # End-to-end entry point
├── data/
│   └── README.md            # Instructions for data placement
└── src/
    ├── __init__.py
    ├── data_loader.py       # Loads and inspects Excel LFQ data
    ├── effect_size.py       # Computes Cohen's d from log2 LFQ intensities
    └── power_analysis.py    # Calculates achieved power and required n
```

| File | Description |
|------|-------------|
| `src/data_loader.py` | Loads and inspects Excel data files, reads LFQ headers |
| `src/effect_size.py` | Computes Cohen's *d* from log2-transformed LFQ intensities |
| `src/power_analysis.py` | Calculates achieved power and required n for target power |
| `run_analysis.py` | End-to-end entry point running the full analysis pipeline |

---

## Dependencies
- `openpyxl`
- `numpy`
- `scipy`

---

## Citation

If referencing this analysis, please cite the associated dissertation:

> Newark, I. (2026). *Effects of systemic bacterial infection on the hippocampal proteome in a mouse model of Alzheimer's disease*. BSc Neuroscience Dissertation, University of Nottingham.
