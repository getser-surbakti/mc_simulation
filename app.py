import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Streamlit app interface
st.markdown("<h1 style='text-align: center; color:rgb(2, 3, 129);'>Simulasikan Harga Saham Pilihanmu disini</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;font-size:20px; color: rgba(4, 120, 155, 0.95);'>Monte Carlo Simulation - Brownian Motion</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; color: #555;'>Tool ini adalah aplikasi untuk memprediksi pergerakan harga saham menggunakan simulasi Monte Carlo dan Gerak Brown. Pengguna dapat memasukkan parameter seperti harga saham sekarang, estimasi return saham, volatilitas, dan jangka waktu dan estimasi tingkat inflasi, lalu melihat proyeksi harga saham di masa depan dalam bentuk grafik.</p>", unsafe_allow_html=True)


#input nama saham
stock_name = st.text_input("Kode Saham yang mau di simulasikan: ", value='PT. TAKSU CAPITAL')
st.markdown(f'**Kode Saham:**<span style="color:rgba(4, 120, 155, 0.95;"> *{stock_name}.*</span>', unsafe_allow_html=True)

# Currency format
def format_currency(value):
    return f"Rp {value:,.0f}".replace(',', '.')

# Initial Stock Price User Inputs
S0 = st.number_input("Harga Saham Sekarang:", value=1000)  # initial stock price
# Display the formatted stock price in Rupiah
formatted_S0 = format_currency(S0)
st.markdown(f'**Harga Saham:**<span style="color:rgba(4, 120, 155, 0.95;">*{formatted_S0}.*</span>',  unsafe_allow_html=True)

# Start Input
start_year = st.number_input("Tahun awal simulasi:", value=2025)
st.markdown(f'**Tahun Awal:**<span style="color:rgba(4, 120, 155, 0.95;"> *{start_year}.*</span>', unsafe_allow_html=True)

# Expected Return
mu = st.number_input(" Expected Return Tahunan Saham berapa?", value=0.08)  # nominal expected return (drift)
st.markdown(f'**Expected Return:**<span style="color:rgba(4, 120, 155, 0.95;"> *{mu*100:.0f} persen.*</span>', unsafe_allow_html=True)

# Volatility
sigma = st.number_input("Volatilitas Sahamnya berapa?", value=0.5)  # volatility
def classify_volatility(sigma):
    if sigma < 0.2:
        return "LOW (Harga aset stabil dan berubah sedikit)"
    elif sigma < 0.5:
        return "MODERATE (Harga aset berubah moderat, tidak terlalu ekstrem)"
    else:
        return "HIGH (Harga aset berubah cepat dan signifikan, risiko lebih tinggi)"
volatility_level = classify_volatility(sigma)
st.markdown(f'**Level Volatilitas:**<span style="color:rgba(4, 120, 155, 0.95;"> *{volatility_level}.*</span>', unsafe_allow_html=True)

# Rentang Simulasi
T = st.number_input("Rentang Waktu simulasi berapa tahun?", value=10)  # time horizon in years
st.markdown(f'**Rentang Simulasi:**<span style="color:rgba(4, 120, 155, 0.95;"> *{T} tahun.*</span>', unsafe_allow_html=True)

# Jumlah Simulasi
M = st.number_input("Jumlah Simulasi:", value=1, min_value=1)  # number of simulations (paths)
st.markdown(f'**Jumlah Simulasi:**<span style="color:rgba(4, 120, 155, 0.95;"> *{M} simulasi.*</span>', unsafe_allow_html=True)

# Tingkat Inflasi
inflation_rate = st.number_input("Tingkat Inflasi kira-kira berapa?", value=0.03)  # inflation rate
st.markdown(f'**Expected Return:**<span style="color:rgba(4, 120, 155, 0.95;"> *{inflation_rate*100:.0f} persen.*</span>', unsafe_allow_html=True)

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

# Create the years array
years = start_year + t  # Add years to the time array

# Visualization with Plotly
fig = go.Figure()

for i in range(M):
    fig.add_trace(go.Scatter(x=years, y=simulations[i], mode='lines', name=f'Simulation {i+1}'))

fig.update_layout(
    title={
        'text': f'Prediksi saham {stock_name} {T} tahun kedepan',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24}
    },
    xaxis_title='Year',
    yaxis_title='Stock Price',
    xaxis=dict(
        tickvals=np.arange(start_year, start_year + T),
        ticktext=np.arange(start_year, start_year + T)
    ),
    hovermode='x unified'
)


# Display the plot in the Streamlit app
st.plotly_chart(fig)

# Calculate and display the average of the endpoint of all simulations
average_endpoint = np.mean(simulations[:, -1])
formatted_average_endpoint = format_currency(average_endpoint)
st.markdown(f'''
    <div style="border: 2px solid rgb(2, 3, 129); padding: 10px; border-radius: 5px; background-color: #f9f9f9; text-align: center; font-size: 24px;">
        <strong>Rata-rata harga akhir dari semua simulasi:</strong> <span style="color: red;">{formatted_average_endpoint}</span>
    </div>
''', unsafe_allow_html=True)
