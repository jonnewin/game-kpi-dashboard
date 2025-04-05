import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime

# ------------------- Game & Company Mapping ------------------- #
game_data = [
    {"game": "Ragnarok M", "company": "Gravity", "ticker": "GRVY"},
    {"game": "Puzzle & Dragons", "company": "Gungho", "ticker": "3765.T"},
    {"game": "Dungeon & Fighter", "company": "Nexon", "ticker": "3659.T"},
]
games_df = pd.DataFrame(game_data)

# ------------------- Sample KPI Time Series Data ------------------- #
kpi_data = pd.DataFrame([
    {"date": "2025-04-01", "game": "Ragnarok M", "app_rank": 14, "twitch_viewers": 21000, "reddit_mentions": 120},
    {"date": "2025-04-02", "game": "Ragnarok M", "app_rank": 12, "twitch_viewers": 22500, "reddit_mentions": 130},
    {"date": "2025-04-03", "game": "Ragnarok M", "app_rank": 10, "twitch_viewers": 24000, "reddit_mentions": 140},
    {"date": "2025-04-01", "game": "Puzzle & Dragons", "app_rank": 20, "twitch_viewers": 5000, "reddit_mentions": 40},
    {"date": "2025-04-02", "game": "Puzzle & Dragons", "app_rank": 18, "twitch_viewers": 5100, "reddit_mentions": 45},
    {"date": "2025-04-03", "game": "Puzzle & Dragons", "app_rank": 17, "twitch_viewers": 5200, "reddit_mentions": 48},
    {"date": "2025-04-01", "game": "Dungeon & Fighter", "app_rank": 9, "twitch_viewers": 30500, "reddit_mentions": 245},
    {"date": "2025-04-02", "game": "Dungeon & Fighter", "app_rank": 8, "twitch_viewers": 31200, "reddit_mentions": 250},
    {"date": "2025-04-03", "game": "Dungeon & Fighter", "app_rank": 7, "twitch_viewers": 31800, "reddit_mentions": 260},
])
kpi_data["date"] = pd.to_datetime(kpi_data["date"])

# ------------------- Sample Catalyst Events ------------------- #
catalysts = pd.DataFrame([
    {"date": "2025-04-15", "event": "Launch – SEA", "subject": "Ragnarok Origin"},
    {"date": "2025-05-01", "event": "Earnings", "subject": "Gungho"},
])

# ------------------- Streamlit Dashboard ------------------- #
st.title("🎮 Gaming KPI Tracker & Catalyst Dashboard")

st.header("📊 Game KPIs (Latest Day)")
latest_kpis = kpi_data.sort_values("date").groupby("game").tail(1)
st.dataframe(latest_kpis.merge(games_df, on="game"))

st.header("📅 Upcoming Catalysts")
catalysts["date"] = pd.to_datetime(catalysts["date"])
catalysts = catalysts.sort_values("date")
st.dataframe(catalysts)

st.header("💹 Company Fundamentals")
for entry in game_data:
    ticker = entry["ticker"]
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        st.subheader(f"{entry['company']} ({ticker})")
        st.markdown(f"**Market Cap:** ${info.get('marketCap', 'N/A'):,}")
        st.markdown(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
        st.markdown(f"**Price:** ${info.get('currentPrice', 'N/A')}")
    except Exception as e:
        st.warning(f"Failed to fetch data for {ticker}: {e}")

# ------------------- KPI Trends Chart ------------------- #
st.header("📈 Game KPI Trends")
selected_game = st.selectbox("Select a game", kpi_data["game"].unique())
filtered_data = kpi_data[kpi_data["game"] == selected_game]
st.line_chart(filtered_data.set_index("date")[["app_rank", "twitch_viewers"]])
