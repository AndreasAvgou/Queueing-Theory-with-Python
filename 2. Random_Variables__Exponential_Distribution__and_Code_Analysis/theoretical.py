import numpy as np

def get_cdf_exp(x, lam):
    """
    Calculates the Cumulative Distribution Function (CDF).
    F(x) = 1 - e^(-lambda * x)
    """
    return 1 - np.exp(-lam * x)

def get_pdf_exp(x, lam):
    """
    Calculates the Probability Density Function (PDF).
    f(x) = lambda * e^(-lambda * x)
    """
    return lam * np.exp(-lam * x)

def get_tail_exp(x, lam):
    """
    Calculates the Tail Probability (Survival Function).
    P(X > x) = e^(-lambda * x)
    """
    return np.exp(-lam * x)