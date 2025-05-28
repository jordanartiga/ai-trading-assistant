# full_dashboard.py — Fully Rebuilt for Functional UI

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

st.set_page_config(page_title="📈 AI Trading Assistant", layout="wide")

st.markdown("""
<style>
body, .reportview-container { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
.sidebar .sidebar-content { background-color: #161b22; }
.block-container { padding: 0rem 3rem; }
.stButton>button { background-color: #238636; color: white; border-radius: 8px; padding: 10px 20px; font-weight: bold; }
.stButton>button:hover { background-color: #2ea043; }
.metric { color: #4caf50; }
.section-title { font-size: 1.4rem; font-weight: bold; margin-top: 1rem; margin-bottom: 0.5rem; }
.card { background-color: #161b22; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
.card-header { font-weight: bold; margin-bottom: 0.5rem; color: #58a6ff; }
.card-content { color: #c9d1d9; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='color:white;'>📈 AI Trading Assistant</h1>", unsafe_allow_html=True)
st.sidebar.markdown("""<div><a href="#live">Live</a><br><a href="#dashboard">Dashboard</a><br><a href="#news">News</a><br><a href="#settings">Settings</a></div>""", unsafe_allow_html=True)
refresh = st.sidebar.selectbox("Auto Refresh:", ["Off", "1s", "5s", "10s"])
refresh_map = {"Off": 0, "1s": 1000, "5s": 5000, "10s": 10000}
interval = refresh_map[refresh]
if interval > 0:
    st_autorefresh(interval=interval, key="refresh")

uploaded_file = st.sidebar.file_uploader("Upload Trade Log", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded: {uploaded_file.name}")
else:
    default_path = os.path.join(os.path.dirname(__file__), "test_trade_log.csv")
    if os.path.exists(default_path):
        df = pd.read_csv(default_path)
    else:
        st.warning("No trade log found. Upload a CSV.")
        df = pd.DataFrame({'Strategy': [], 'Result': [], 'Confidence': [], 'Prediction': []})

if 'Strategy' not in df.columns or df['Strategy'].isnull().all():
    df = apply_strategy_detection(df)
if 'Confidence' not in df.columns:
    df['Confidence'] = [random.randint(70, 95) for _ in range(len(df))]
if 'Prediction' not in df.columns:
    df['Prediction'] = [random.choice(['Up', 'Down']) for _ in range(len(df))]

news_df = get_today_news()
if not news_df.empty:
    latest_news = news_df.iloc[0]
    st.markdown(f"""<div class='card'><div class='card-header'>🚨 News Alert</div><div class='card-content'>{latest_news['Title']} (Impact: {latest_news['Impact']}) — {latest_news['Time']}</div></div>""", unsafe_allow_html=True)
else:
    st.markdown("<div class='card'><div class='card-header'>✅ No major news</div></div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("<div class='section-title'>📈 Live MES Chart</div>", unsafe_allow_html=True)
    df_live = get_live_mes_data()
    if not df_live.empty:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_live['Time'], open=df_live['Open'], high=df_live['High'], low=df_live['Low'], close=df_live['Close'], increasing_line_color='#4caf50', decreasing_line_color='#f44336'))
        fig.update_layout(height=500, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117', font=dict(color='#c9d1d9'))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='section-title'>🧾 Trade Log</div>", unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)
with col2:
    st.markdown("<div class='section-title'>🧠 Strategy & AI</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><div class='card-header'>Strategy Detector</div><div class='card-content'>{render_strategy_panel()}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><div class='card-header'>AI Prediction</div><div class='card-content'>{render_prediction_panel()}</div></div>", unsafe_allow_html=True)
    if 'Result' in df.columns:
        win_rate = (df['Result'].str.lower() == 'win').mean() * 100
        st.markdown(f"<div class='card'><div class='card-header'>Win Rate</div><div class='card-content'>{win_rate:.1f}%</div></div>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>⚙️ Settings</div>", unsafe_allow_html=True)
