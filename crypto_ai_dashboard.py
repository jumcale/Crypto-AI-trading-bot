
# Install with: pip install streamlit pandas
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from binance.client import Client
from ta.momentum import RSIIndicator
from ta.trend import MACD

API_KEY = 'YOUR_TESTNET_API_KEY'
API_SECRET = 'YOUR_TESTNET_SECRET_KEY'
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

symbol = 'BTCUSDT'
interval = '1h'
limit = 100

st.set_page_config(page_title="Crypto AI Bot Dashboard", layout="wide")

st.title("📊 Crypto AI Trading Bot Dashboard")

def fetch_data():
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df.set_index('timestamp', inplace=True)
    return df

def add_indicators(df):
    df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df.dropna(inplace=True)
    return df

df = fetch_data()
df = add_indicators(df)

st.subheader("Price Chart")
st.line_chart(df[['close']])

st.subheader("RSI & MACD Indicators")
st.line_chart(df[['rsi', 'macd', 'macd_signal']])

st.subheader("Latest Data Snapshot")
st.dataframe(df.tail(10))
