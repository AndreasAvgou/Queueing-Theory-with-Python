import numpy as np

# Random number generator for reproducibility
rng = np.random.default_rng(12345)

def simulate_mm1(lam: float, mu: float, n: int = 100_000, warmup: int = 5_000):
    """
    Simulates an M/M/1 queue with rates lam (arrival) and mu (service).
    Returns estimates for W, L, Wq, Lq, and the empirical rho.
    """
    # Stability condition check: lambda < mu
    if lam >= mu:
        raise ValueError("Stability condition required: lambda < mu")

    # Generate arrival times (exponential distribution with mean 1/lambda)
    # rng.exponential() expects 'scale', which is 1/lambda
    arrivals = np.cumsum(rng.exponential(1/lam, size=n))

    # Service times (exponential distribution with mean 1/mu)
    services = rng.exponential(1/mu, size=n)

    start_service = np.empty(n)
    depart = np.empty(n)

    # Time when the server becomes free (last departure time)
    server_free_at = 0.0
    
    for i in range(n):
        start_service[i] = max(arrivals[i], server_free_at)
        depart[i] = start_service[i] + services[i]
        server_free_at = depart[i]

    waits = start_service - arrivals      # Wq (waiting time in queue)
    sojourn = depart - arrivals           # W (total time in system)

    # Discard initial customers (warmup period)
    sl = slice(warmup, n)
    W_hat = sojourn[sl].mean()
    Wq_hat = waits[sl].mean()

    # Little's Law for L, Lq
    L_hat = lam * W_hat
    Lq_hat = lam * Wq_hat

    # Empirical utilization (fraction of time server was busy)
    total_busy_time = services[warmup:].sum()
    total_sim_time = depart[-1] - arrivals[warmup]
    rho_empirical = total_busy_time / total_sim_time
    
    return W_hat, L_hat, Wq_hat, Lq_hat, rho_empirical