import numpy as np
from theoretical import get_cdf_exp
from empirical import calculate_ecdf

def calculate_mle_lambda(mean_empirical):
    """
    Maximum Likelihood Estimation (MLE) for lambda.
    For Exponential distribution: lambda_hat = 1 / mean
    """
    return 1.0 / float(mean_empirical)

def calculate_ks_statistic(samples, lam_hat):
    """
    Calculates the Kolmogorov-Smirnov (KS) statistic.
    Measures the maximum distance between the ECDF and the theoretical CDF.
    """
    s_sorted, ecdf_vals = calculate_ecdf(samples)
    
    # Calculate theoretical CDF using the estimated lambda
    cdf_vals = get_cdf_exp(s_sorted, lam_hat)
    
    # Find maximum absolute difference
    ks_stat = float(np.max(np.abs(ecdf_vals - cdf_vals)))
    return ks_stat