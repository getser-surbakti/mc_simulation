import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit app interface
st.title('Monte Carlo Simulation for Stock Price Prediction')

# User Inputs
S0 = st.number_input("Enter the initial stock price:", value=1010)  # initial stock price
mu = st.number_input("Enter the expected return:", value=0.08)  # expected return (drift)
sigma = st.number_input("Enter the volatility:", value=0.5)  # volatility
T = st.number_input("Enter the time horizon in years:", value=10)  # time horizon in years
M = st.number_input("Enter the number of simulations:", value=1, min_value=1)  # number of simulations (paths)

# Derived Parameters
dt = 1/252  # daily steps (assuming 252 trading days in a year)
N = int(T / dt)  # number of time steps
t = np.linspace(0, T, N)

# Monte Carlo simulation for M paths
np.random.seed(42)  # For reproducibility
simulations = np.zeros((M, N))

for i in range(M):
    # Generate random normal variables for each time step
    random_shocks = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt), size=N)
    
    # Calculate the stock price path (GBM formula)
    price_path = S0 * np.exp(np.cumsum(random_shocks))  # cumsum for cumulative sum (simulating price)
    simulations[i] = price_path

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, simulations.T, color='blue', alpha=0.8)  # Transpose to get the time on x-axis
ax.set_title('Prediksi saham TUGU 10 tahun kedepan')
ax.set_xlabel('Year')
ax.set_ylabel('Stock Price')

# Modify x-axis to show years starting from 2025
start_year = 2025
years = start_year + t  # Add years to the time array
ax.set_xticks(np.linspace(0, T, T))
ax.set_xticklabels(np.arange(start_year, start_year + T))  # Show years at intervals
ax.grid(True)

# Display the plot in the Streamlit app
st.pyplot(fig)
