import numpy as np
import matplotlib.pyplot as plt
from theoretical import get_pdf_exp, get_cdf_exp
from empirical import calculate_ecdf

def plot_pdf_vs_histogram(samples, lam):
    """
    Plots the Histogram of samples vs the Theoretical PDF.
    """
    xs = np.linspace(0, np.quantile(samples, 0.99), 400)
    plt.figure(figsize=(8, 5))
    plt.hist(samples, bins=60, density=True, alpha=0.6, label='Samples (Histogram)', color='skyblue', edgecolor='black')
    plt.plot(xs, get_pdf_exp(xs, lam), 'r-', linewidth=2, label='Theoretical PDF')
    plt.xlabel('x')
    plt.ylabel('Density')
    plt.title(f'Exponential({lam}) — PDF vs Samples')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_cdf_vs_ecdf(samples, lam):
    """
    Plots the Empirical CDF vs the Theoretical CDF.
    """
    xs = np.linspace(0, np.quantile(samples, 0.99), 400)
    s_sorted, y_ecdf = calculate_ecdf(samples)
    
    plt.figure(figsize=(8, 5))
    plt.step(s_sorted, y_ecdf, where='post', label='Empirical CDF', color='blue')
    plt.plot(xs, get_cdf_exp(xs, lam), 'r--', linewidth=2, label='Theoretical CDF')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('CDF vs ECDF')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_qq(samples, lam):
    """
    Creates a Q-Q (Quantile-Quantile) plot to check fit.
    """
    qs = np.linspace(0.01, 0.99, 99)
    emp_quantiles = np.quantile(samples, qs)
    # Theoretical quantiles for Exp(lambda) = -ln(1-p) / lambda
    theo_quantiles = -np.log(1 - qs) / lam
    
    plt.figure(figsize=(6, 6))
    plt.scatter(theo_quantiles, emp_quantiles, s=15, color='purple', alpha=0.7)
    
    # 45-degree reference line
    max_val = max(theo_quantiles.max(), emp_quantiles.max())
    plt.plot([0, max_val], [0, max_val], 'k--', label='Perfect Fit')
    
    plt.xlabel('Theoretical Quantiles')
    plt.ylabel('Empirical Quantiles')
    plt.title('Exponential Q–Q Plot')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()