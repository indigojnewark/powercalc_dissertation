# Data

Place the following files in this directory before running the analysis:

| File | Description |
|------|-------------|
| `IJN_Data.xlsx` | MaxQuant LFQ output with one sheet per pairwise group comparison |
| `IJN_Provision.xlsx` | Provision/metadata file (optional; inspected but not required for power calc) |

## Sheet structure (IJN_Data.xlsx)

Each sheet corresponds to a pairwise group comparison:

| Sheet | Groups compared |
|-------|-----------------|
| `AD-ADinfec` | AD vs AD+Infection (key comparison for power analysis) |
| `AD-Ctrl` | AD vs Control |
| `AD-infec` | AD vs Infection |
| `Adinfec-Ctrl` | AD+Infection vs Control |
| `ADinfec-infec` | AD+Infection vs Infection |
| `infec-Ctrl` | Infection vs Control |

Columns 0-2 contain LFQ intensities for Group A (e.g. AD1, AD2, AD3) and columns 3-5 for Group B.

## Data privacy

These files are excluded from version control via `.gitignore` as they contain unpublished experimental proteomic data. Do not commit raw data files to this repository.
