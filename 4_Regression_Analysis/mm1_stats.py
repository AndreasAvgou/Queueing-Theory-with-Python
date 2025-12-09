import numpy as np
from dataclasses import dataclass
from mm1_simulation import simulate_mm1_one_run

@dataclass
class NqMaxStats:
    rho: float
    nq_max_mean: float
    nq_max_std: float

def estimate_nq_max_for_rho(rho, mu=1.0, R=30, max_time=2000.0, warmup_time=200.0, seed=123):
    """
    Estimates the mean Nq-max(rho) by running R independent simulation runs.
    
    Returns:
        NqMaxStats: An object containing rho, mean, and std dev of max queue length.
    """
    lmbda = rho * mu
    rng = np.random.default_rng(seed)

    nq_max_values = []
    for i in range(R):
        nq_max = simulate_mm1_one_run(lmbda, mu, max_time=max_time, warmup_time=warmup_time, rng=rng)
        nq_max_values.append(nq_max)

    nq_max_values = np.array(nq_max_values)
    return NqMaxStats(
        rho=rho,
        nq_max_mean=nq_max_values.mean(),
        nq_max_std=nq_max_values.std(ddof=1)
    )