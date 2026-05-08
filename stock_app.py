import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(page_title="Ultra Stock Analytics", layout="wide")
st.title(" Ultra Pro Stock Analytics Terminal")

ticker_symbol = st.sidebar.text_input("Enter Ticker", "TSLA")
period = st.sidebar.selectbox("Period", ["1mo", "6mo", "1y", "2y", "5y", "max"])

df = yf.download(ticker_symbol, period=period)

if not df.empty:
 
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                       vertical_spacing=0.05, 
                       subplot_titles=('Price Action', 'Volume', 'RSI (Relative Strength Index)'),
                       row_width=[0.2, 0.2, 0.6])

    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], line=dict(color='yellow', width=1.5), name="MA50"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], line=dict(color='blue', width=1.5), name="MA200"), row=1, col=1)

    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='orange'), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='magenta', width=1.5), name="RSI"), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1) 
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1) 

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=900)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Data Summary"):
        st.dataframe(df.tail(10))
else:
    st.error("Invalid Ticker!")
