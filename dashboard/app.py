import streamlit as st
import pandas as pd
import joblib
from src.fetch_price import fetch_price_history
from src.sentiment import apply_sentiment
from src.collect_data import collect_all

st.set_page_config(page_title="CryptoSense DSS", layout="wide")

st.title("📊 CryptoSense: Sentiment-Based DSS")

if st.button("Fetch Latest Data"):
    new_data = collect_all()
    st.success("Fetched real-time data!")

if st.button("Predict Market Direction"):
    model = joblib.load("model/random_forest.pkl")
    df = pd.read_csv("data/feature_data.csv")
    latest = df.iloc[-1][["sentiment", "price"]].values.reshape(1, -2)
    prediction = model.predict(latest)[0]

    decision = "BUY" if prediction == 1 else "SELL"
    st.metric(label="Decision", value=decision)
    st.write("Latest Sentiment:", df.iloc[-1]["sentiment"])

