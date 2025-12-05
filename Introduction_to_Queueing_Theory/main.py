import mm1_lib as mm1

# --- 1. Define Parameters ---
lmbda = 4.0  # customers/hour
mu = 6.0     # customers/hour
lambda_test_values = [4.0, 5.0, 5.5, 5.8]

# --- 2. Run Basic Scenario ---
mm1.print_full_report(lmbda, mu)

# --- 3. Run Sensitivity Analysis ---
mm1.run_sensitivity_analysis(lambda_test_values, mu)

# --- 4. Show Plots ---
# Note: The script will pause here until plot windows are closed.
mm1.show_plots(mu)