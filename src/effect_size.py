"""effect_size.py

Computes Cohen's d (pooled SD formulation) from log2-transformed
LFQ intensity values across proteins.
"""

import numpy as np


def cohens_d_log2(group_a: list, group_b: list):
    """
    Compute Cohen's d between two groups on log2-transformed LFQ intensities.

    Uses the pooled standard deviation formulation:
        d = |mean_B - mean_A| / s_pooled

    where s_pooled = sqrt(((n_a-1)*s_a^2 + (n_b-1)*s_b^2) / (n_a+n_b-2))

    Parameters
    ----------
    group_a : list of float
        Raw (non-log) LFQ intensities for group A.
    group_b : list of float
        Raw (non-log) LFQ intensities for group B.

    Returns
    -------
    float or None
        Cohen's d, or None if pooled SD cannot be computed
        (e.g. fewer than 2 observations in either group).
    """
    log_a = np.log2(group_a)
    log_b = np.log2(group_b)
    n_a, n_b = len(log_a), len(log_b)

    if n_a < 2 or n_b < 2:
        return None

    pooled_var = (
        (n_a - 1) * np.var(log_a, ddof=1) + (n_b - 1) * np.var(log_b, ddof=1)
    ) / (n_a + n_b - 2)

    pooled_sd = np.sqrt(pooled_var)

    if pooled_sd == 0:
        return None

    return abs(np.mean(log_b) - np.mean(log_a)) / pooled_sd


def compute_effect_sizes(protein_data: list) -> list:
    """
    Compute Cohen's d for each protein across all valid group pairs.

    Parameters
    ----------
    protein_data : list of tuple
        Each element is (group_a_vals, group_b_vals).

    Returns
    -------
    list of float
        Cohen's d values; proteins where d cannot be computed are excluded.
    """
    ds = []
    for group_a, group_b in protein_data:
        d = cohens_d_log2(group_a, group_b)
        if d is not None:
            ds.append(d)
    return ds


def summarise_effect_sizes(ds: list) -> None:
    """Print descriptive statistics for a list of Cohen's d values."""
    arr = np.array(ds)
    print(f"Proteins with computable Cohen's d : {len(arr)}")
    print(f"  Median      : {np.median(arr):.3f}")
    print(f"  Mean        : {np.mean(arr):.3f}")
    print(f"  25th pctile : {np.percentile(arr, 25):.3f}")
    print(f"  75th pctile : {np.percentile(arr, 75):.3f}")
