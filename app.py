import streamlit as st
from binance_data import prepare_informer_input
from informer_model import process_informer_input
import plotly.graph_objects as go
from PIL import Image
import time
import numpy as np
import os

# Load the logo image
logo_path = os.path.join("C:\\Users\\Kaushik Nerusu\\OneDrive\\Pictures\\cryptosense", "crypto_logo.png")
logo = Image.open(logo_path)

# Set page configuration with a wide layout and custom title
st.set_page_config(layout="wide", page_title="CryptoSense - Empowering your Crypto Journey")

# Splash screen function
def show_splash_screen():
    st.image(logo, width=300)
    st.title("CryptoSense")
    st.subheader("Empowering your Crypto Journey")
    time.sleep(3)  # Display for 3 seconds
    st.empty()  # Clear the splash screen

# Custom CSS for Binance-like dark theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e2126;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #1e2126;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #f0b90b;
        color: #000000;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #e0a90b;
    }
    .stMetric>label {
        color: #ffffff;
    }
    .stMetric>value {
        color: #f0b90b;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display splash screen on first load
if 'splash_shown' not in st.session_state:
    show_splash_screen()
    st.session_state.splash_shown = True

# Sidebar for Binance-like navigation
st.sidebar.header("CryptoSense Dashboard")
crypto_options = ["Bitcoin", "Ethereum", "Dogecoin"]
timeframe_options = ["1h", "1d", "1w"]
selected_crypto = st.sidebar.selectbox("Select Cryptocurrency", crypto_options)
selected_timeframe = st.sidebar.selectbox("Select Timeframe", timeframe_options)

# Button to trigger prediction
if st.sidebar.button("Get Prediction"):
    # Prepare the Informer input
    informer_input = prepare_informer_input(selected_crypto, selected_timeframe)
    
    if informer_input:
        # Process the input to get prediction and recommendation
        result = process_informer_input(informer_input)
        
        if result:
            # Extract results
            sentiment_score = informer_input["sentiment_score"]
            current_price = informer_input["current_price"]
            predicted_price = result["predicted_price"]
            recommendation = result["recommendation"]
            timeframe = result["timeframe"]

            # Simulate historical price data (10 data points) with some variance
            np.random.seed(42)  # For reproducibility
            historical_prices = np.linspace(current_price * 0.98, current_price, 10)
            historical_prices += np.random.normal(0, current_price * 0.01, 10)  # Add noise
            timestamps = np.arange(-9, 1) * ({"1h": 1, "1d": 24, "1w": 168}[timeframe] / 10)

            # Create candlestick-like graph with Plotly
            fig = go.Figure(data=[go.Scatter(x=timestamps, y=historical_prices, mode='lines', name='Historical Price')])
            fig.add_trace(go.Scatter(x=[0, 1], y=[current_price, predicted_price], mode='lines+markers', name='Prediction',
                                    line=dict(dash='dash')))
            fig.update_layout(
                title=f"{selected_crypto} Price Prediction ({timeframe})",
                yaxis_title="Price (USDT)",
                template="plotly_dark",
                xaxis_title="Time (hours)",
                yaxis=dict(tickformat=".2f")
            )

            # Display results
            st.subheader("Market Overview")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Current Price", f"{current_price:.2f} USDT")
                st.metric("Sentiment Score", f"{sentiment_score:.4f}")
                st.metric("Predicted Price", f"{predicted_price:.2f} USDT")
            
            with col2:
                st.metric("Recommendation", recommendation)
                st.text(f"Timeframe: {timeframe}")

            # Display the graph
            st.plotly_chart(fig)

        else:
            st.error("Failed to process the prediction.")
    else:
        st.error("Failed to prepare the input data.")