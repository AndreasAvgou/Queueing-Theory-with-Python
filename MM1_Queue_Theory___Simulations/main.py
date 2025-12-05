import numpy as np
import pandas as pd
from mm1_simulation import simulate_mm1
from mm1_theory import theory_mm1
from mm1_plots import generate_plots

def main():
    print("Starting M/M/1 simulation...")

    # Parameters
    mu = 1.0
    rhos = np.linspace(0.05, 0.95, 19)
    n_customers = 120_000
    warmup = 10_000

    # Lists to store results
    sim_W, sim_L, sim_Wq, sim_Lq, sim_rho_emp = [], [], [], [], []
    th_W, th_L, th_Wq, th_Lq = [], [], [], []

    # Main Calculation Loop
    for rho in rhos:
        lam = rho * mu
        
        # Call Simulation
        W_hat, L_hat, Wq_hat, Lq_hat, rho_emp = simulate_mm1(lam, mu, n=n_customers, warmup=warmup)
        
        sim_W.append(W_hat)
        sim_L.append(L_hat)
        sim_Wq.append(Wq_hat)
        sim_Lq.append(Lq_hat)
        sim_rho_emp.append(rho_emp)

        # Call Theory
        W, L, Wq, Lq = theory_mm1(lam, mu)
        
        th_W.append(W)
        th_L.append(L)
        th_Wq.append(Wq)
        th_Lq.append(Lq)

    # Convert to numpy arrays (optional, but good for calculations)
    sim_W = np.array(sim_W)
    sim_L = np.array(sim_L)
    sim_Wq = np.array(sim_Wq)
    sim_Lq = np.array(sim_Lq)
    th_W = np.array(th_W)
    th_L = np.array(th_L)
    th_Wq = np.array(th_Wq)
    th_Lq = np.array(th_Lq)

    print("Scan complete.")

    # Create Dictionary for Plotting
    results_data = {
        'sim_W': sim_W, 'th_W': th_W,
        'sim_L': sim_L, 'th_L': th_L,
        'sim_Wq': sim_Wq, 'th_Wq': th_Wq,
        'sim_Lq': sim_Lq, 'th_Lq': th_Lq,
        'sim_rho_emp': sim_rho_emp
    }

    # Generate and Show Plots
    generate_plots(rhos, results_data)

    # Create and Print DataFrame (Summary Table)
    df = pd.DataFrame({
        'rho': rhos,
        'T_sim': sim_W,
        'T_theory': th_W,
        'L_sim': sim_L,
        'L_theory': th_L,
        'Wq_sim': sim_Wq,
        'Wq_theory': th_Wq,
        'Lq_sim': sim_Lq,
        'Lq_theory': th_Lq,
        'rho_empirical': sim_rho_emp,
        'rho_input': rhos,
        'rho_error': np.array(sim_rho_emp) - rhos,
    })

    print("\nSummary Results Table (First 20 rows):")
    print(df.head(20).to_string())

if __name__ == "__main__":
    main()