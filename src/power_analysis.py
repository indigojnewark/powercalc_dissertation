import numpy as np
from scipy import stats


def power_two_sample_ttest(d: float, n: int, alpha: float = 0.05) -> float:
    """
    Compute power of a two-sample t-test given Cohen's d, n per group, and alpha.

    Uses the non-central t-distribution.
    """
    df = 2 * n - 2
    t_crit = stats.t.ppf(1 - alpha / 2, df)
    ncp = d * np.sqrt(n / 2)
    power = (
        1 - stats.nct.cdf(t_crit, df, ncp)
        + stats.nct.cdf(-t_crit, df, ncp)
    )
    return power


def n_for_target_power(
    d: float,
    target_power: float = 0.80,
    alpha: float = 0.05,
    max_n: int = 300
):
    """
    Find the minimum n per group required to achieve target power.

    Returns '>max_n' as a string if not achievable within max_n.
    """
    for n in range(2, max_n + 1):
        if power_two_sample_ttest(d, n, alpha) >= target_power:
            return n
    return f">{max_n}"


def print_power_report(
    effect_sizes: dict,
    actual_ns: list,
    alpha: float = 0.05
) -> None:
    """
    Print a formatted power analysis report.

    Args:
        effect_sizes: dict of {label: d_value}
        actual_ns: list of actual per-group sample sizes to evaluate
        alpha: significance threshold
    """
    print("=" * 60)
    print("POST-HOC POWER ANALYSIS")
    print(f"Alpha = {alpha}, two-sided two-sample t-test")
    print("=" * 60)

    print(f"\n--- Achieved power at actual sample sizes ---")
    for label, d in effect_sizes.items():
        powers = [
            f"n={n}: {power_two_sample_ttest(d, n, alpha):.2f}"
            for n in actual_ns
        ]
        print(f"  {label} (d={d:.3f}): {' | '.join(powers)}")

    print(f"\n--- n per group required for 80% power ---")
    for label, d in effect_sizes.items():
        n_req = n_for_target_power(d, target_power=0.80, alpha=alpha)
        print(f"  {label} (d={d:.3f}): n = {n_req}")
