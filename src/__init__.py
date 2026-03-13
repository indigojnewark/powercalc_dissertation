"""src

Power analysis package for:
  'Effects of systemic bacterial infection on the hippocampal proteome
   in a mouse model of Alzheimer's disease'

Modules
-------
data_loader     : Load and inspect MaxQuant LFQ Excel output
effect_size     : Compute Cohen's d from log2-transformed LFQ intensities
power_analysis  : Post-hoc power calculations using non-central t-distribution
"""

__version__ = "1.0.0"
__author__ = "Indigo Newark"

from .data_loader import inspect_workbook, load_sheet, get_lfq_values
from .effect_size import cohens_d_log2, compute_effect_sizes, summarise_effect_sizes
from .power_analysis import power_two_sample_ttest, n_for_target_power, print_power_report

__all__ = [
    "inspect_workbook",
    "load_sheet",
    "get_lfq_values",
    "cohens_d_log2",
    "compute_effect_sizes",
    "summarise_effect_sizes",
    "power_two_sample_ttest",
    "n_for_target_power",
    "print_power_report",
]
