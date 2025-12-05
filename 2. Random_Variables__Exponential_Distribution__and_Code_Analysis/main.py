import numpy as np
# Importing functions from our modules
from theoretical import get_tail_exp
from empirical import calculate_empirical_tail
from estimation import calculate_mle_lambda, calculate_ks_statistic
from plotting import plot_pdf_vs_histogram, plot_cdf_vs_ecdf, plot_qq

def main():
    # --- Settings ---
    lam = 3.0          # Lambda parameter (rate)
    n = 20000          # Sample size
    rng = np.random.default_rng(12345)

    print("--- 1. Sampling & Basic Moments ---")
    # Sampling from Exp(lambda)
    # Note: numpy uses 'scale' which is 1/lambda
    samples = rng.exponential(scale=1/lam, size=n)

    # Theoretical quantities
    E_theory = 1 / lam
    Var_theory = 1 / (lam**2)

    # Empirical estimations
    E_emp = samples.mean()
    Var_emp = samples.var(ddof=1)

    print({
        'lambda_param': lam,
        'Mean_Theory': E_theory,
        'Mean_Empirical': float(E_emp),
        'Variance_Theory': Var_theory,
        'Variance_Empirical': float(Var_emp)
    })
    print("-" * 50)

    # --- Tail Probability Analysis ---
    print("\n--- 2. Tail Probability Analysis P(X > t) ---")
    thresholds = [0.1, 0.3, 0.5, 1.0]
    results = []
    
    print(f"{'t':<5} | {'Theory':<10} | {'Empirical':<10} | {'Diff':<10}")
    for t in thresholds:
        th_val = get_tail_exp(t, lam)
        emp_val = calculate_empirical_tail(samples, t)
        diff = emp_val - th_val
        print(f"{t:<5} | {th_val:.5f}    | {emp_val:.5f}     | {diff:.5f}")
    print("-" * 50)

    # --- Visualization ---
    print("\n--- 3. Generating Plots ---")
    print("Generating PDF Histogram...")
    plot_pdf_vs_histogram(samples, lam)
    
    print("Generating CDF Comparison...")
    plot_cdf_vs_ecdf(samples, lam)
    
    print("Generating Q-Q Plot...")
    plot_qq(samples, lam)
    print("-" * 50)

    # --- Estimation & Goodness of Fit ---
    print("\n--- 4. Parameter Estimation (MLE) & KS Test ---")
    
    # Calculate MLE for lambda
    lam_hat = calculate_mle_lambda(E_emp)
    
    print(f"True Lambda: {lam}")
    print(f"Estimated Lambda (MLE): {lam_hat:.5f}")

    # Calculate KS Statistic
    ks_stat = calculate_ks_statistic(samples, lam_hat)
    print(f"KS Statistic (against MLE): {ks_stat:.5f}")

if __name__ == "__main__":
    main()