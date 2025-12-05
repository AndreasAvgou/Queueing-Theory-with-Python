#  Queueing Theory with Python

This repository serves as a comprehensive toolkit for analyzing Stochastic Models and Queueing Systems. It bridges the gap between theoretical mathematical formulas and empirical validation through Python simulations.

The project is designed to help students and researchers understand how random variables behave and how queueing systems (specifically **M/M/1**) perform under various loads.

## 📂 Repository Structure

The project is organized into three distinct modules, each contained in its own directory:

```text
├── 01_Exponential_Distribution/   # Module 1: Random Variables Analysis
│   ├── theoretical.py             # Exact mathematical formulas (PDF, CDF)
│   ├── empirical.py               # Empirical calculations from samples
│   ├── estimation.py              # Statistical estimation (MLE, KS Test)
│   ├── plotting.py                # Visualization tools (Histograms, Q-Q plots)
│   └── main.py                    # Execution script for distribution analysis
│
├── 02_MM1_Basics/                 # Module 2: Basic M/M/1 Formulas
│   └── mm1_lib.py                 # Library for calculating L, Lq, W, Wq
│
├── 03_MM1_Simulation/             # Module 3: Full Discrete Event Simulation
│   ├── mm1_simulation.py          # Core simulation engine (Vectorized)
│   ├── mm1_theory.py              # Theoretical verification formulas
│   ├── mm1_plots.py               # Comparison plotting tools
│   └── main.py                    # Main execution script (Iterates rho 0.05-0.95)
│
├── README.md                      # Project Documentation
└── requirements.txt               # Dependencies
```

## 🛠️ Installation & Requirements

To run the code across all modules, you need Python installed along with the following libraries:

 * NumPy: For numerical operations and random sampling.
 * Matplotlib: For generating comparison plots.
 * Pandas: For data aggregation and tabular reporting.

Install dependencies via pip:

```
pip install numpy matplotlib pandas
```

## 📘 Module 1: Exponential Distribution Analysis
Folder: 01_Exponential_Distribution/

This module focuses on the Exponential Distribution, the fundamental building block of queueing theory used to model inter-arrival and service times.
Features
* Stochastic Sampling: Generates random variables based on the exponential PDF $f(x) = \lambda e^{-\lambda x}$.
* Tail Probability: Calculates $P(X > t)$ to determine the likelihood of waiting longer than a specific time.
* Goodness of Fit:
  * MLE (Maximum Likelihood Estimation): Estimates $\lambda$ from raw data ($\hat{\lambda} = 1 / \bar{X}$).
  * KS Test: Computes the Kolmogorov-Smirnov statistic to verify if the data matches the theoretical model.

Usage

Navigate to the folder and run the analysis script:

```
cd 01_Exponential_Distribution
python main.py
```

## 📙 Module 2: Basic M/M/1 Metrics

Folder: 02_MM1_Basics/

This module provides a lightweight library for calculating the steady-state performance metrics of a simple M/M/1 queue.
Key Metrics

* Utilization ($\rho$): The percentage of time the server is busy ($\rho = \lambda / \mu$).
* Little's Law: Implements the fundamental theorem $L = \lambda W$.
* Formulas Implemented:
  * $L = \rho / (1 - \rho)$ (Avg customers in system).
  * $W = 1 / (\mu - \lambda)$ (Avg time in system).

Usage

You can import this library into your own scripts to perform quick calculations:
```
Python
from mm1_lib import calculate_metrics

metrics = calculate_metrics(lmbda=4, mu=6)
print(f"Average Wait Time: {metrics['W']} hours")
```
## 📕 Module 3: M/M/1 Simulation & Validation

Folder: 03_MM1_Simulation/

This module implements a full Discrete Event Simulation (DES) to validate the theoretical formulas of the M/M/1 model across various traffic intensities.
Features

* Simulation Logic:
  * Generates arrivals using np.cumsum on exponential inter-arrival times.
  * Calculates departure times based on server availability: start_service = max(arrival, previous_departure).
* Warm-up Period: Discards the initial batch of customers (transient state) to ensure accurate steady-state statistics.
* Comparative Analysis:
  * Runs the simulation for multiple values of $\rho$ (0.05 to 0.95).
  * Compares Simulated results vs. Theoretical curves for $W, L, W_q, L_q$.

Usage

Navigate to the folder and run the simulation suite:
```
cd 03_MM1_Simulation
python main.py
```
Output:The script generates 5 interactive plots and prints a summary DataFrame comparing theory and simulation:
```
Summary Results Table:
    rho     T_sim  T_theory     L_sim  L_theory  ...
0  0.05  1.05321   1.05263   0.05266   0.05263  ...
1  0.10  1.11245   1.11111   0.11125   0.11111  ...
...
```
🧠 Theoretical Background

Kendall's Notation

The systems analyzed here follow the notation A/B/s/K/N/D:
* M/M/1: Markovian Arrivals (Poisson), Markovian Service (Exponential), 1 Server.

Stability Condition
For the system to reach a steady state (and for the queue not to explode), the arrival rate must be less than the service rate:

  $$\lambda < \mu \quad \text{or} \quad \rho < 1$$
  
Little's Law

Valid for all stable queueing systems:
    $$L = \lambda \cdot W$$
    
The average number of customers in the system is equal to the arrival rate multiplied by the average time a customer spends in the system.
