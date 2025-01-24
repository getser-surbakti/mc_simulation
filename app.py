import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit app interface
st.title('Simulasikan Harga Saham Pilihanmu disini')
st.subheader('Monte Carlo Simulation')
st.write("Tool ini adalah aplikasi untuk memprediksi pergerakan harga saham menggunakan simulasi Monte Carlo. Pengguna dapat memasukkan parameter seperti harga saham sekarang, estimasi return saham, volatilitas, dan jangka waktu dan estimasi tingkat inflasi, lalu melihat proyeksi harga saham di masa depan dalam bentuk grafik.")
#input nama saham
stock_name =st.text_input("Kode Saham yang mau di simulasikan: ", value='PT. TAKSU CAPITAL')


# Currency format
def format_currency(value):
    return f"Rp {value:,.0f}".replace(',', '.')

# Initial Stock Price User Inputs
S0 = st.number_input("Harga Saham Sekarang:", value=1000)  # initial stock price
# Display the formatted stock price in Rupiah
formatted_S0 = format_currency(S0)
st.write(f": {formatted_S0}")

# Other input
start_year = st.number_input("Tahun awal simulasi:", value=2025)
mu = st.number_input(" Expected Return Tahunan Saham berapa?", value=0.08)  # nominal expected return (drift)
sigma = st.number_input("Volatilitas Sahamnya berapa?", value=0.5)  # volatility
T = st.number_input("Rentang Waktu simulasi berapa tahun?", value=10)  # time horizon in years
M = st.number_input("Jumlah Simulasi:", value=1, min_value=1)  # number of simulations (paths)
inflation_rate = st.number_input("Tingkat Inflasi kira-kira berapa?", value=0.03)  # inflation rate

# Derived Parameters
dt = 1 / 252  # daily steps (assuming 252 trading days in a year)
N = int(T / dt)  # number of time steps
t = np.linspace(0, T, N)

# Adjusted expected return after accounting for inflation (real return)
real_mu = (1 + mu) / (1 + inflation_rate) - 1  # Adjust for inflation to get real return

# Monte Carlo simulation for M paths
np.random.seed(42)  # For reproducibility
simulations = np.zeros((M, N))

for i in range(M):
    # Generate random normal variables for each time step
    random_shocks = np.random.normal(loc=real_mu * dt, scale=sigma * np.sqrt(dt), size=N)
    
    # Calculate the stock price path (GBM formula)
    price_path = S0 * np.exp(np.cumsum(random_shocks))  # cumsum for cumulative sum (simulating price)
    simulations[i] = price_path

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, simulations.T, color='blue', alpha=0.8)  # Transpose to get the time on x-axis
ax.set_title(f'Prediksi saham {stock_name} {T} tahun kedepan')
ax.set_xlabel('Year')
ax.set_ylabel('Stock Price')

# Modify x-axis to show years starting from 2025
years = start_year + t  # Add years to the time array
ax.set_xticks(np.linspace(0, T, T))
ax.set_xticklabels(np.arange(start_year, start_year + T))  # Show years at intervals
ax.grid(True)

# Display the plot in the Streamlit app
st.pyplot(fig)
