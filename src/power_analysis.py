"""power_analysis.py

Post-hoc power analysis for two-sample t-tests using the non-central
t-distribution. Computes achieved power at observed sample sizes and
the minimum n required to reach a target power level.
"""

import numpy as np
from scipy import stats


def power_two_sample_ttest(d: float, n: int, alpha: float = 0.05) -> float:
    """
    Compute the power of a two-sample t-test.

    Uses the non-central t-distribution to calculate the probability of
    correctly rejecting H0 given an effect size d and n per group.

    Parameters
    ----------
    d : float
        Cohen's d (standardised effect size).
    n : int
        Sample size per group (assumed equal).
    alpha : float
        Two-tailed significance threshold (default: 0.05).

    Returns
    -------
    float
        Statistical power (probability of rejecting H0 when H1 is true).
    """
    df = 2 * n - 2
    t_crit = stats.t.ppf(1 - alpha / 2, df)
    ncp = d * np.sqrt(n / 2)  # non-centrality parameter
    power = (
        1 - stats.nct.cdf(t_crit, df, ncp)
        + stats.nct.cdf(-t_crit, df, ncp)
    )
    return float(power)


def n_for_target_power(
    d: float,
    target_power: float = 0.80,
    alpha: float = 0.05,
    max_n: int = 300,
):
    """
    Find the minimum n per group required to achieve a target power level.

    Parameters
    ----------
    d : float
        Cohen's d (standardised effect size).
    target_power : float
        Desired power level (default: 0.80).
    alpha : float
        Two-tailed significance threshold (default: 0.05).
    max_n : int
        Upper bound on the search (default: 300).

    Returns
    -------
    int or str
        Minimum n per group, or the string '>max_n' if not achievable
        within the search range.
    """
    for n in range(2, max_n + 1):
        if power_two_sample_ttest(d, n, alpha) >= target_power:
            return n
    return f">{max_n}"


def print_power_report(
    effect_sizes: dict,
    actual_ns: list,
    alpha: float = 0.05,
) -> None:
    """
    Print a formatted post-hoc power analysis report.

    Parameters
    ----------
    effect_sizes : dict
        Mapping of {label: Cohen's d value} for each scenario to evaluate.
    actual_ns : list of int
        Actual per-group sample sizes from the study.
    alpha : float
        Two-tailed significance threshold (default: 0.05).
    """
    sep = "=" * 60
    print(sep)
    print("POST-HOC POWER ANALYSIS")
    print(f"Alpha = {alpha}, two-sided two-sample t-test")
    print(sep)

    print("\n--- Achieved power at actual sample sizes ---")
    for label, d in effect_sizes.items():
        powers = [
            f"n={n}: {power_two_sample_ttest(d, n, alpha):.2f}"
            for n in actual_ns
        ]
        print(f"  {label} (d={d:.3f}): {' | '.join(powers)}")

    print("\n--- n per group required for 80% power ---")
    for label, d in effect_sizes.items():
        n_req = n_for_target_power(d, target_power=0.80, alpha=alpha)
        print(f"  {label} (d={d:.3f}): n = {n_req}")
