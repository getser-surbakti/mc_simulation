import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Custom CSS dengan gaya futuristik ala Elon Musk, font merah dan emas
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        body {
            background: linear-gradient(135deg, #1a1a1a, #2c3e50);
            color: #ecf0f1;
            font-family: 'Orbitron', sans-serif;
        }
        .stApp {
            background: transparent;
        }
        h1 {
            text-align: center;
            color: #e74c3c; /* Merah */
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 0 25px rgba(231, 76, 60, 0.5), 0 0 50px rgba(231, 76, 60, 0.2);
            text-transform: uppercase;
            letter-spacing: 4px;
            font-weight: 700;
            text-shadow: 0 0 15px rgba(231, 76, 60, 0.7);
            animation: pulse 2s infinite;
        }
        h2 {
            text-align: center;
            font-size: 24px;
            color: #f1c40f; /* Emas */
            letter-spacing: 3px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(241, 196, 15, 0.5);
        }
        p {
            text-align: justify;
            color: #e74c3c; /* Merah */
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border: 1px solid rgba(231, 76, 60, 0.4);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
        }
        .stTextInput > div > input, .stNumberInput > div > input {
            background: rgba(255, 255, 255, 0.05);
            border: 3px solid #3498db;
            color: #ecf0f1;
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
            transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
        }
        .stTextInput > div > input:focus, .stNumberInput > div > input:focus {
            border-color: #e74c3c;
            box-shadow: 0 0 15px rgba(231, 76, 60, 0.7);
            transform: scale(1.02);
        }
        .stButton > button {
            background: #e74c3c;
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 15px 25px;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 700;
            transition: transform 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 0 15px rgba(231, 76, 60, 0.5);
        }
        .stButton > button:hover {
            background: #c0392b;
            transform: scale(1.05);
            box-shadow: 0 0 25px rgba(231, 76, 60, 0.8);
        }
        .stMarkdown span {
            color: #f1c40f; /* Emas */
            text-shadow: 0 0 5px rgba(241, 196, 15, 0.5);
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 25px rgba(231, 76, 60, 0.5), 0 0 50px rgba(231, 76, 60, 0.2); }
            50% { box-shadow: 0 0 35px rgba(231, 76, 60, 0.7), 0 0 70px rgba(231, 76, 60, 0.4); }
            100% { box-shadow: 0 0 25px rgba(231, 76, 60, 0.5), 0 0 50px rgba(231, 76, 60, 0.2); }
        }
    </style>
""", unsafe_allow_html=True)

# Header dengan font merah
st.markdown("""
    <h1>
        SIMULATOR HARGA SAHAM
    </h1>
""", unsafe_allow_html=True)

# Subheader dengan font emas dan deskripsi dengan font merah
st.markdown("<h2>Hyper Monte Carlo - Quantum Brownian Thrust</h2>", unsafe_allow_html=True)
st.markdown("""
    <p>
        Nyalakan mesin simulasi ini untuk memproyeksikan lintasan saham ke masa depan. Dengan teknologi Hyper Monte Carlo dan dorongan Quantum Brownian, masukkan parameter saham Anda—harga saham saat ini, tenaga penggerak return, turbulensi volatilitas, durasi investasi saham, dan entropi inflasi—untuk menembus batas keuntungan maksimal.
    </p>
""", unsafe_allow_html=True)

# Input nama saham
stock_name = st.text_input("Kode Target Saham:", value='PT. TAKSU CAPITAL')
st.markdown(f'**Identitas Misi:** <span>*{stock_name}*</span>', unsafe_allow_html=True)

# Format mata uang
def format_currency(value):
    return f"Rp {value:,.0f}".replace(',', '.')

# Input Harga Saham Sekarang
S0 = st.number_input("Harga Awal Saham (Rp):", value=1000)
formatted_S0 = format_currency(S0)
st.markdown(f'**Harga Awal:** <span>*{formatted_S0}*</span>', unsafe_allow_html=True)

# Input Tahun Awal
start_year = st.number_input("Tahun Peluncuran:", value=2025)
st.markdown(f'**Tahun Mulai:** <span>*{start_year}*</span>', unsafe_allow_html=True)

# Expected Return
mu = st.number_input("Tenaga Penggerak Tahunan:", value=0.08)
st.markdown(f'**Daya Thrust:** <span>*{mu*100:.0f} persen*</span>', unsafe_allow_html=True)

# Volatilitas
sigma = st.number_input("Turbulensi Saham:", value=0.5)
def classify_volatility(sigma):
    if sigma < 0.2:
        return "STABIL (Pergerakan saham mulus, gangguan minimal)"
    elif sigma < 0.5:
        return "MODERAT (Pergerakan saham dinamis, fluktuasi terkendali)"
    else:
        return "KHAOS (Pergerakan saham liar, risiko tinggi)"
volatility_level = classify_volatility(sigma)
st.markdown(f'**Status Turbulensi:** <span>*{volatility_level}*</span>', unsafe_allow_html=True)

# Rentang Simulasi
T = st.number_input("Durasi Investasi (Tahun):", value=10)
st.markdown(f'**Jarak Tempuh:** <span>*{T} tahun*</span>', unsafe_allow_html=True)

# Jumlah Simulasi
M = st.number_input("Jumlah Lintasan Simulasi:", value=1, min_value=1)
st.markdown(f'**Jumlah Simulasi:** <span>*{M} lintasan*</span>', unsafe_allow_html=True)

# Tingkat Inflasi
inflation_rate = st.number_input("Entropi Inflasi:", value=0.03)
st.markdown(f'**Faktor Entropi:** <span>*{inflation_rate*100:.0f} persen*</span>', unsafe_allow_html=True)

# Parameter Derivatif
dt = 1 / 252  # Langkah harian (252 hari perdagangan per tahun)
N = int(T / dt)  # Jumlah langkah waktu
t = np.linspace(0, T, N)

# Return riil setelah inflasi
real_mu = (1 + mu) / (1 + inflation_rate) - 1

# Simulasi Monte Carlo untuk M lintasan
np.random.seed(42)
simulations = np.zeros((M, N))

for i in range(M):
    random_shocks = np.random.normal(loc=real_mu * dt, scale=sigma * np.sqrt(dt), size=N)
    price_path = S0 * np.exp(np.cumsum(random_shocks))
    simulations[i] = price_path

# Array tahun
years = start_year + t

# Visualisasi dengan Plotly yang futuristik
fig = go.Figure()

for i in range(M):
    fig.add_trace(go.Scatter(
        x=years,
        y=simulations[i],
        mode='lines',
        name=f'Lintasan {i+1}',
        line=dict(color='#e74c3c', width=2.5),
        hoverinfo='x+y',
        opacity=0.8
    ))

fig.update_layout(
    title={
        'text': f'Proyeksi Lintasan Saham {stock_name} - {T} Tahun',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 28, 'color': '#e74c3c', 'family': 'Orbitron'}  # Merah
    },
    xaxis_title='Tahun',
    yaxis_title='Harga Saham (Rp)',
    xaxis=dict(
        tickvals=np.arange(start_year, start_year + T),
        ticktext=np.arange(start_year, start_year + T),
        tickfont={'color': '#f1c40f', 'size': 14},  # Emas
        titlefont={'color': '#f1c40f', 'size': 16},  # Emas
        gridcolor='rgba(255, 255, 255, 0.15)',
        zerolinecolor='#3498db',
        zerolinewidth=1
    ),
    yaxis=dict(
        tickfont={'color': '#f1c40f', 'size': 14},  # Emas
        titlefont={'color': '#f1c40f', 'size': 16},  # Emas
        gridcolor='rgba(255, 255, 255, 0.15)',
        zerolinecolor='#3498db',
        zerolinewidth=1
    ),
    plot_bgcolor='rgba(0, 0, 0, 0.95)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font={'color': '#ecf0f1', 'family': 'Orbitron'},
    hovermode='x unified',
    hoverlabel={'bgcolor': 'rgba(231, 76, 60, 0.9)', 'font': {'color': '#ffffff', 'size': 14, 'family': 'Orbitron'}},
    transition={'duration': 1000, 'easing': 'cubic-in-out'}
)

# Tampilkan grafik
st.plotly_chart(fig, use_container_width=True)

# Hitung dan tampilkan rata-rata titik akhir dengan font merah dan emas
average_endpoint = np.mean(simulations[:, -1])
formatted_average_endpoint = format_currency(average_endpoint)
st.markdown(f'''
    <div style="border: 3px solid #e74c3c; padding: 20px; border-radius: 10px; background: rgba(255, 255, 255, 0.05); text-align: center; font-size: 28px; box-shadow: 0 0 20px rgba(231, 76, 60, 0.5); animation: pulse 2s infinite;">
        <strong style="color: #e74c3c;">Rata-rata Titik Akhir:</strong> <span style="color: #f1c40f; text-shadow: 0 0 10px rgba(241, 196, 15, 0.7);">{formatted_average_endpoint}</span>
    </div>
''', unsafe_allow_html=True)