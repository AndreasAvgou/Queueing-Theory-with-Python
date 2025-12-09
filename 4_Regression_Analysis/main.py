import numpy as np
import mm1_stats
import mm1_models
import mm1_plots

def main():
    # --- Simulation Parameters ---
    rho_values = np.arange(0.1, 0.95, 0.05)
    mu = 1.0
    R = 30

    print("--- Starting M/M/1 Simulations ---")
    stats_list = []
    for rho in rho_values:
        stats = mm1_stats.estimate_nq_max_for_rho(
            rho, mu=mu, R=R, max_time=2000.0, warmup_time=200.0, seed=123 + int(rho*100)
        )
        stats_list.append(stats)
        print(f"rho = {rho:.2f}, Nq-max (mean) = {stats.nq_max_mean:.2f}, std = {stats.nq_max_std:.2f}")

    # Prepare data arrays
    rho_arr = np.array([s.rho for s in stats_list])
    nq_max_mean_arr = np.array([s.nq_max_mean for s in stats_list])
    nq_max_std_arr = np.array([s.nq_max_std for s in stats_list])
    nq_theory_arr = mm1_models.calculate_theoretical_nq(rho_arr)

    # --- 1. Basic Comparison Plot ---
    mm1_plots.plot_empirical_vs_theoretical(rho_arr, nq_max_mean_arr, nq_max_std_arr, nq_theory_arr)

    # --- 2. Linear Regression Model ---
    print("\n--- Linear Regression: Nq-max ~ a + b * Nq(rho) ---")
    X = nq_theory_arr.reshape(-1, 1)
    y = nq_max_mean_arr
    lin_reg, a, b, r2 = mm1_models.fit_linear_model(X, y)
    
    print(f"Model: Nq-max approx {a:.3f} + {b:.3f} * Nq(rho)")
    print(f"R^2 = {r2:.3f}")
    
    mm1_plots.plot_linear_regression(X, y, lin_reg)
    
    # Residuals for Linear Model
    nq_max_pred_lin = lin_reg.predict(X)
    residuals_lin = nq_max_mean_arr - nq_max_pred_lin
    mm1_plots.plot_residuals(nq_theory_arr, residuals_lin, "Theoretical Nq(rho)", "Residuals: Linear Model")
    mm1_plots.plot_residuals(rho_arr, residuals_lin, "rho", "Residuals vs rho (Linear Model)")


    # --- 3. Power-Law Model (Log-Linear) ---
    print("\n--- Power-law Model: Nq-max ~ A / (1 - rho)^B ---")
    pl_reg, A, B, r2_pl, X_pl, Y_pl = mm1_models.fit_power_law_log_space(rho_arr, nq_max_mean_arr)
    
    print(f"Model: Nq-max approx {A:.3f} / (1 - rho)^{B:.3f}")
    print(f"R^2 (log-space) = {r2_pl:.3f}")
    
    mm1_plots.plot_power_law_log_space(X_pl, Y_pl, pl_reg)
    mm1_plots.plot_power_law_original_space(rho_arr, nq_max_mean_arr, nq_max_std_arr, A, B)
    
    # Residuals for Power-Law Model
    nq_max_pred_pl = A / (1.0 - rho_arr)**B
    residuals_pl = nq_max_mean_arr - nq_max_pred_pl
    mm1_plots.plot_residuals(rho_arr, residuals_pl, "rho", "Residuals: Power-law Model")


    # --- 4. Non-Linear Weighted Fit (Advanced) ---
    print("\n--- Non-linear Weighted Power-law Model (with Offset) ---")
    popt, perr, r2_nl, y_pred_nl = mm1_models.fit_nonlinear_power_law(rho_arr, nq_max_mean_arr, nq_max_std_arr)
    A_hat, B_hat, C_hat = popt
    
    print("Model: Nq-max(rho) approx C + A / (1 - rho)^B")
    print(f"A = {A_hat:.3f} +/- {perr[0]:.3f}")
    print(f"B = {B_hat:.3f} +/- {perr[1]:.3f}")
    print(f"C = {C_hat:.3f} +/- {perr[2]:.3f}")
    print(f"R^2 (original space) = {r2_nl:.3f}")

    mm1_plots.plot_nonlinear_fit(rho_arr, nq_max_mean_arr, nq_max_std_arr, popt)
    
    residuals_nl = nq_max_mean_arr - y_pred_nl
    mm1_plots.plot_residuals(rho_arr, residuals_nl, "rho", "Residuals: Non-linear Weighted Model")

if __name__ == "__main__":
    main()