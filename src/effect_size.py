import numpy as np


def cohens_d_log2(group_a: list, group_b: list):
    """
    Compute Cohen's d between two groups on log2-transformed LFQ intensities.

    Returns None if pooled SD cannot be computed (e.g. n < 2 in either group).
    """
    log_a = np.log2(group_a)
    log_b = np.log2(group_b)
    n_a, n_b = len(log_a), len(log_b)

    if n_a < 2 or n_b < 2:
        return None

    pooled_sd = np.sqrt(
        ((n_a - 1) * np.var(log_a, ddof=1) + (n_b - 1) * np.var(log_b, ddof=1))
        / (n_a + n_b - 2)
    )

    if pooled_sd == 0:
        return None

    return abs(np.mean(log_b) - np.mean(log_a)) / pooled_sd


def compute_effect_sizes(protein_data: list) -> list:
    """
    Compute Cohen's d for each protein across all valid group pairs.

    Args:
        protein_data: list of (group_a_vals, group_b_vals) tuples

    Returns:
        List of Cohen's d values (only proteins with computable d included)
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
    print(f"Proteins with computable Cohen's d: {len(arr)}")
    print(f"  Median:      {np.median(arr):.3f}")
    print(f"  Mean:        {np.mean(arr):.3f}")
    print(f"  25th pctile: {np.percentile(arr, 25):.3f}")
    print(f"  75th pctile: {np.percentile(arr, 75):.3f}")
