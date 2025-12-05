import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_metrics(lmbda: float, mu: float):
    """
    Calculates and returns M/M/1 metrics.
    """
    if lmbda <= 0 or mu <= 0:
        raise ValueError("Lambda and mu must be positive.")
    if lmbda >= mu:
        raise ValueError("Stability requires lambda < mu.")
    
    rho = lmbda / mu
    L = rho / (1 - rho)
    Lq = rho**2 / (1 - rho)
    W = 1 / (mu - lmbda)
    Wq = Lq / lmbda
    
    return {"rho": rho, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

def print_full_report(lmbda: float, mu: float):
    """
    Performs calculations and prints a detailed report.
    """
    try:
        m = calculate_metrics(lmbda, mu)
        print("\n=== M/M/1 Calculations ===")
        print(f"lambda = {lmbda:.4f}  |  mu = {mu:.4f}")
        print(f"rho (utilization) = lambda/mu = {m['rho']:.4f}")
        print(f"L  (avg number in system)        = {m['L']:.4f}")
        print(f"Lq (avg number in queue)         = {m['Lq']:.4f}")
        print(f"W  (avg time in system) [hours]  = {m['W']:.4f}")
        print(f"Wq (avg time in queue)  [hours]  = {m['Wq']:.4f}")
        print(f"W  ≈ {m['W']*60:.1f} mins,  Wq ≈ {m['Wq']*60:.1f} mins")
    except ValueError as e:
        print(f"Error: {e}")

def run_sensitivity_analysis(lambda_values: list, mu: float):
    """
    Runs the scenario with multiple lambda values to demonstrate sensitivity.
    """
    print("\n=== Sensitivity Analysis (Playing with values) ===")
    print(f"Effect when lambda approaches mu ({mu}):")
    print(f"{'lambda':<8} {'rho':<8} {'L':<8} {'Lq':<8} {'W (h)':<8} {'Wq (h)':<8}")
    print("-" * 60)
    
    for l in lambda_values:
        try:
            m = calculate_metrics(l, mu)
            print(f"{l:<8.1f} {m['rho']:<8.3f} {m['L']:<8.3f} {m['Lq']:<8.3f} {m['W']:<8.3f} {m['Wq']:<8.3f}")
        except ValueError as e:
            print(f"{l:<8.1f} Error: {e}")

def show_plots(mu_fixed: float):
    """
    Creates and displays the plots (L/Lq and W/Wq).
    """
    print(f"\n[INFO] Generating plots with mu={mu_fixed}...")
    
    # Helper functions for arrays
    def _L(rho): return rho / (1 - rho)
    def _Lq(rho): return rho**2 / (1 - rho)
    def _W(rho, mu): return 1.0 / (mu * (1 - rho))
    def _Wq(rho, mu): return rho / (mu * (1 - rho))

    rho_vals = np.linspace(0.01, 0.95, 200)

    # Figure 1: L and Lq vs rho
    plt.figure(figsize=(10, 5))
    plt.plot(rho_vals, _L(rho_vals), label="L (System)")
    plt.plot(rho_vals, _Lq(rho_vals), label="Lq (Queue)", linestyle="--")
    plt.xlabel("rho (Utilization)")
    plt.ylabel("Count (Number of Customers)")
    plt.title("M/M/1: L and Lq vs rho")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Figure 2: W and Wq vs rho
    plt.figure(figsize=(10, 5))
    plt.plot(rho_vals, _W(rho_vals, mu_fixed), label="W (System Time)")
    plt.plot(rho_vals, _Wq(rho_vals, mu_fixed), label="Wq (Queue Time)", linestyle="--")
    plt.xlabel("rho (Utilization)")
    plt.ylabel("Time (hours)")
    plt.title(f"M/M/1: W and Wq vs rho (mu={mu_fixed})")
    plt.legend()
    plt.grid(True)
    plt.show()