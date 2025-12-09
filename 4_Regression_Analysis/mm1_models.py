import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

def calculate_theoretical_nq(rho_arr):
    """Calculates Theoretical Nq(rho) = rho^2 / (1 - rho)."""
    return rho_arr**2 / (1 - rho_arr)

def fit_linear_model(X, y):
    """
    Fits a linear regression model y = a + b * X.
    Returns intercept (a), coefficient (b), and R^2 score.
    """
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    
    a = lin_reg.intercept_
    b = lin_reg.coef_[0]
    r2 = lin_reg.score(X, y)
    return lin_reg, a, b, r2

def fit_power_law_log_space(rho_arr, nq_max_mean_arr):
    """
    Fits a power-law model Nq-max ~ A / (1 - rho)^B using log-linear regression.
    Filters out zero values to avoid log errors.
    Returns A, B, and R^2.
    """
    mask = nq_max_mean_arr > 0
    rho_pl = rho_arr[mask]
    nq_max_pl = nq_max_mean_arr[mask]

    X_pl = np.log(1.0 / (1.0 - rho_pl)).reshape(-1, 1)  # log(1/(1-rho))
    Y_pl = np.log(nq_max_pl)                            # log(Nq-max)

    lin_reg = LinearRegression()
    lin_reg.fit(X_pl, Y_pl)

    alpha = lin_reg.intercept_
    B = lin_reg.coef_[0]
    A = np.exp(alpha)
    r2 = lin_reg.score(X_pl, Y_pl)
    
    return lin_reg, A, B, r2, X_pl, Y_pl

def powerlaw_offset(rho, A, B, C):
    """
    Non-linear model function: Nq-max(rho) = C + A / (1 - rho)^B.
    """
    return C + A / (1.0 - rho)**B

def fit_nonlinear_power_law(rho_arr, y_data, y_std):
    """
    Fits the non-linear power-law model with offset using scipy.curve_fit.
    Returns optimal parameters (A, B, C), errors, R^2, and predicted y.
    """
    # Handle zero std deviation for weighting
    y_std_safe = y_std.copy()
    if np.any(y_std_safe == 0):
        min_pos = y_std_safe[y_std_safe > 0].min() if np.any(y_std_safe > 0) else 1.0
        y_std_safe[y_std_safe == 0] = min_pos

    # Initial guess
    p0 = [3.0, 1.2, 0.0]

    popt, pcov = curve_fit(
        powerlaw_offset,
        rho_arr,
        y_data,
        p0=p0,
        sigma=y_std_safe,
        absolute_sigma=True,
        maxfev=10000
    )

    A_hat, B_hat, C_hat = popt
    perr = np.sqrt(np.diag(pcov))
    
    # Calculate R^2
    y_pred = powerlaw_offset(rho_arr, *popt)
    ss_res = np.sum((y_data - y_pred)**2)
    ss_tot = np.sum((y_data - np.mean(y_data))**2)
    r2 = 1 - ss_res / ss_tot
    
    return (A_hat, B_hat, C_hat), perr, r2, y_pred