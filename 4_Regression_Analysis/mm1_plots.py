import matplotlib.pyplot as plt
import numpy as np
from mm1_models import powerlaw_offset

# Global plot settings
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['grid.alpha'] = 0.3

def plot_empirical_vs_theoretical(rho_arr, nq_max_mean_arr, nq_max_std_arr, nq_theory_arr):
    plt.figure()
    plt.plot(rho_arr, nq_theory_arr, 's--', label="Theoretical Nq(rho)")
    plt.errorbar(rho_arr, nq_max_mean_arr, yerr=nq_max_std_arr, fmt='o', capsize=4, label="Empirical Nq-max(rho)")
    plt.xlabel("rho")
    plt.ylabel("Queue Length")
    plt.title("Comparison: Theoretical Nq(rho) vs Empirical Nq-max(rho)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_linear_regression(X, y, model):
    x_plot = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_pred_plot = model.predict(x_plot)

    plt.figure()
    plt.scatter(X, y, label="Data (Nq-theory vs Nq-max)")
    plt.plot(x_plot, y_pred_plot, 'r', label="Linear Regression")
    plt.xlabel("Theoretical Nq(rho)")
    plt.ylabel("Nq-max (mean)")
    plt.title("Model: Nq-max ~ a + b * Nq(rho)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_power_law_log_space(X_pl, Y_pl, model):
    x_plot_pl = np.linspace(X_pl.min(), X_pl.max(), 100).reshape(-1, 1)
    y_plot_pl = model.predict(x_plot_pl)

    plt.figure()
    plt.scatter(X_pl, Y_pl, label="Data (log-space)")
    plt.plot(x_plot_pl, y_plot_pl, 'r', label="Linear Regression (log-space)")
    plt.xlabel("ln( 1 / (1 - rho) )")
    plt.ylabel("ln(Nq-max)")
    plt.title("Power-law: Linearity check in log-space")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_power_law_original_space(rho_arr, nq_max_mean_arr, nq_max_std_arr, A, B):
    rho_fine = np.linspace(rho_arr.min(), rho_arr.max(), 200)
    nq_max_model = A / (1.0 - rho_fine)**B

    plt.figure()
    plt.errorbar(rho_arr, nq_max_mean_arr, yerr=nq_max_std_arr, fmt='o', capsize=4, label="Empirical Nq-max(rho)")
    plt.plot(rho_fine, nq_max_model, 'r', label="Power-law Model")
    plt.xlabel("rho")
    plt.ylabel("Nq-max")
    plt.title("Nq-max(rho): Data vs Power-law Model")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_residuals(x_data, residuals, x_label, title):
    plt.figure()
    plt.axhline(0, linestyle='--')
    plt.scatter(x_data, residuals)
    plt.xlabel(x_label)
    plt.ylabel("Residuals (Observed - Model)")
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_nonlinear_fit(rho_data, y_data, y_std, popt):
    rho_fine = np.linspace(rho_data.min(), rho_data.max(), 300)
    y_fine = powerlaw_offset(rho_fine, *popt)

    plt.figure()
    plt.errorbar(rho_data, y_data, yerr=y_std, fmt='o', capsize=4, label="Empirical Nq-max(rho)")
    plt.plot(rho_fine, y_fine, 'r-', linewidth=2, label="Non-linear Weighted Power-law")
    plt.xlabel("rho")
    plt.ylabel("Nq-max")
    plt.title("Nq-max(rho): Data vs Improved Power-law Model")
    plt.grid(True)
    plt.legend()
    plt.show()