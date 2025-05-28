# full_dashboard.py — Advanced UI, Session State, Custom Chart, & Deployment Ready

from strategy_detector_module import render_strategy_panel
from ai_prediction_module import render_prediction_panel
from news_alert_module import get_today_news, format_news_alert
from mes_live_feed import get_live_mes_data
from gpt_strategy_detector import apply_strategy_detection

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
from streamlit_autorefresh import st_autorefresh
import random

# 🔁 Auto Refresh Setup
st.set_page_config(page_title="📈 AI Trading Assistant", layout="wide")

# 📚 Session State Defaults
if 'auto_refresh' not in st.session_state:
    st.session_state['auto_refresh'] = "Off"
if 'strategy_filter' not in st.session_state:
    st.session_state['strategy_filter'] = []

# 📚 Custom CSS & Icons
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>
body, .reportview-container { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
.sidebar .sidebar-content { background-color: #161b22; }
.block-container { padding: 1rem 2rem; }
.stButton>button { background-color: #238636; color: white; border-radius: 8px; padding: 10px 20px; font-weight: bold; }
.stButton>button:hover { background-color: #2ea043; }
.prediction-card { border-left: 5px solid #238636; background-color: #161b22; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: #c9d1d9; display: flex; align-items: center; gap: 10px; }
.alert-card { background-color: #ff4d4d; padding: 10px; border-radius: 10px; color: white; font-weight: bold; display: flex; align-items: center; gap: 10px; }
.gpt-summary { background-color: #1f6feb; padding: 10px; border-radius: 10px; color: white; }
.icon { font-size: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# Sidebar with Session State
st.sidebar.markdown("<div class='sidebar-icons'><a href='#live'><i class='fas fa-chart-line icon'></i> Live</a><a href='#backtest'><i class='fas fa-search icon'></i> Backtest</a><a href='#dashboard'><i class='fas fa-tachometer-alt icon'></i> Dashboard</a><a href='#news'><i class='fas fa-newspaper icon'></i> News</a><a href='#settings'><i class='fas fa-cog icon'></i> Settings</a></div>", unsafe_allow_html=True)

refresh = st.sidebar.selectbox("⏱ Auto Refresh:", ["Off", "1s", "5s", "10s", "30s"], index=["Off", "1s", "5s", "10s", "30s"].index(st.session_state['auto_refresh']))
st.session_state['auto_refresh'] = refresh
refresh_map = {"Off": 0, "1s": 1000, "5s": 5000, "10s": 10000, "30s": 30000}
interval = refresh_map[refresh]
if interval > 0:
    st_autorefresh(interval=interval, key="refresh")

# Load Trade Log
uploaded_file = st.sidebar.file_uploader("📂 Upload Trade Log (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded: {uploaded_file.name}")
else:
    default_path = os.path.join(os.path.dirname(__file__), "test_trade_log.csv")
    if os.path.exists(default_path):
        df = pd.read_csv(default_path)
        st.sidebar.info("Loaded default log.")
    else:
        st.sidebar.error("No CSV uploaded and no test file found.")
        st.stop()

if 'Strategy' not in df.columns or df['Strategy'].isnull().all():
    with st.spinner("🧠 Detecting strategies using GPT..."):
        df = apply_strategy_detection(df)
        st.success("✅ Strategies detected using GPT!")
if 'Confidence' not in df.columns:
    st.warning("'Confidence' column missing. Generating demo confidence.")
    df['Confidence'] = [random.randint(70, 95) for _ in range(len(df))]
if 'Prediction' not in df.columns:
    st.warning("'Prediction' column missing. Generating demo predictions.")
    df['Prediction'] = [random.choice(['Up', 'Down']) for _ in range(len(df))]

news_df = get_today_news()
if not news_df.empty:
    latest_news = news_df.iloc[0]
    st.markdown(f"<div class='alert-card'><i class='fas fa-exclamation-triangle icon'></i> 🚨 <b>News Alert:</b> {latest_news['Title']} (Impact: {latest_news['Impact']}) — {latest_news['Time']}</div>", unsafe_allow_html=True)
else:
    st.info("✅ No major news at this time.")

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    st.markdown("<h2 id='live'>📈 Live</h2>", unsafe_allow_html=True)
    st.subheader("📊 Enhanced MES Chart")
    df_live = get_live_mes_data()
    if all(col in df_live.columns for col in ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']):
        df_live['price'] = df_live[['Open', 'High', 'Low', 'Close']].mean(axis=1)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_live['Time'], open=df_live['Open'], high=df_live['High'], low=df_live['Low'], close=df_live['Close'], increasing_line_color='#4caf50', decreasing_line_color='#f44336', line=dict(width=1)))
        fig.update_layout(height=600, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117', font=dict(color='#c9d1d9'), xaxis=dict(gridcolor='#444', showline=True, linewidth=1, linecolor='#888'), yaxis=dict(gridcolor='#444', showline=True, linewidth=1, linecolor='#888'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("🧾 Trade Log Preview")
    st.dataframe(df.head(10), use_container_width=True)

with col2:
    st.markdown("<h2 id='dashboard'>📊 Dashboard</h2>", unsafe_allow_html=True)
    st.markdown(render_strategy_panel(), unsafe_allow_html=True)
    st.markdown("### 🤖 AI Prediction")
    for i, row in df.iterrows():
        card_class = "prediction-card" if row['Prediction'] == "Up" else "alert-card"
        icon = "<i class='fas fa-arrow-up'></i>" if row['Prediction'] == "Up" else "<i class='fas fa-arrow-down'></i>"
        st.markdown(f"<div class='{card_class}'>{icon} <b>Prediction:</b> {row['Prediction']}<br><b>Confidence:</b> {row['Confidence']}%<br>Forecast: Next 5-10 min<br><i>Actionable signal detected. Review for entry opportunities.</i></div>", unsafe_allow_html=True)

with col3:
    st.markdown("<h2 id='news'>📰 News</h2>", unsafe_allow_html=True)
    st.markdown("### 🧠 GPT Trade Summary")
    st.markdown("<div class='gpt-summary'><i class='fas fa-robot'></i> 📢 This trade was a bullish trap reversal during CPI release. Volume spike + delta divergence confirmed entry.</div>", unsafe_allow_html=True)
    if 'Result' in df.columns:
        win_rate = (df['Result'].str.lower() == 'win').mean() * 100
        st.metric("✅ Win Rate", f"{win_rate:.1f}%")
        win_rate_by_strategy = df.groupby('Strategy')['Result'].apply(lambda x: (x.str.lower() == 'win').mean() * 100).sort_values(ascending=False)
        fig, ax = plt.subplots()
        win_rate_by_strategy.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_ylabel('Win Rate (%)')
        ax.set_title('Win Rate by Strategy')
        st.pyplot(fig)
    st.markdown("<div class='alert-card'><i class='fas fa-sync-alt'></i> 📢 <b>New Reversal Alert:</b><br>Long at 5445.75, stop at 5441.00</div>", unsafe_allow_html=True)

st.markdown("<h2 id='settings'>⚙️ Settings</h2>", unsafe_allow_html=True)
