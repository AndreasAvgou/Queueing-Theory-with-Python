import numpy as np

def calculate_empirical_tail(samples, t):
    """
    Calculates the fraction of samples greater than threshold t.
    """
    return float((samples > t).mean())

def calculate_ecdf(samples):
    """
    Computes the Empirical Cumulative Distribution Function (ECDF) for plotting.
    Returns sorted samples and their corresponding y-values (probabilities).
    """
    s_sorted = np.sort(samples)
    y_values = np.arange(1, len(s_sorted) + 1) / len(s_sorted)
    return s_sorted, y_values