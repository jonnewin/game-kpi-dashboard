import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime

# Game & Company Mapping
game_data = [
    {"game": "Ragnarok M", "company": "Gravity", "ticker": "GRVY"},
    {"game": "Puzzle & Dragons", "company": "Gungho", "ticker": "3765.T"},
    {"game": "Dungeon & Fighter", "company": "Nexon", "ticker": "3659.T"},
]
games_df = pd.DataFrame(game_data)

# Sample KPI Data
kpi_data = pd.DataFrame([
    {"game": "Ragnarok M", "app_rank": 12, "twitch_viewers": 22500, "reddit_mentions": 130},
    {"game": "Puzzle & Dragons", "app_rank": 18, "twitch_viewers": 5100, "reddit_mentions": 45},
    {"game": "Dungeon & Fighter", "app_rank": 8, "twitch_viewers": 31200, "reddit_mentions": 250},
])

# Sample Catalyst Events
catalysts = pd.DataFrame([
    {"date": "2025-04-15", "event": "Launch – SEA", "subject": "Ragnarok Origin"},
    {"date": "2025-05-01", "event": "Earnings", "subject": "Gungho"},
])

# Streamlit UI
st.title("🎮 Gaming KPI Tracker & Catalyst Dashboard")

st.header("📊 Game KPIs")
st.dataframe(kpi_data.merge(games_df, on="game"))

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
