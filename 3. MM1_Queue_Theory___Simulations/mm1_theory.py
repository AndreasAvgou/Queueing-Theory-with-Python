def theory_mm1(lam: float, mu: float):
    """
    Theoretical formulas for M/M/1 (rho = lambda/mu < 1).
    Returns W, L, Wq, Lq.
    """
    rho = lam / mu
    # Stability check
    if rho >= 1.0:
        return None, None, None, None
        
    W = 1.0 / (mu - lam)              # Average time in system
    L = rho / (1.0 - rho)             # Average number in system
    Wq = rho / (mu - lam)             # Average time in queue
    Lq = (rho**2) / (1.0 - rho)       # Average number in queue
    
    return W, L, Wq, Lq