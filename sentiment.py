import os
from dotenv import load_dotenv
import numpy as np
from transformers import pipeline
import requests
import streamlit as st

def is_streamlit_running():
    try:
        from streamlit.runtime import get_instance
        return get_instance() is not None
    except:
        return False

def safe_streamlit_warning(message):
    if is_streamlit_running():
        st.warning(message)
    else:
        print(f"WARNING: {message}")

def safe_streamlit_error(message):
    if is_streamlit_running():
        st.error(message)
    else:
        print(f"ERROR: {message}")

def safe_streamlit_info(message):
    if is_streamlit_running():
        st.info(message)
    else:
        print(f"INFO: {message}")

@st.cache_data
def get_newsapi_sentiment(keyword, api_key):
    """
    Fetch real-time news articles from NewsAPI and compute sentiment with FinBERT.
    
    Args:
        keyword (str): Cryptocurrency name (e.g., 'Bitcoin').
        api_key (str): NewsAPI key from .env.
    
    Returns:
        float: Average sentiment score (-1 to 1), or 0 if no data.
    """
    try:
        sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={api_key}"
        print(f"DEBUG: Fetching NewsAPI URL: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            safe_streamlit_warning(f"NewsAPI request failed (status {response.status_code}). Response: {response.text}")
            return 0
        
        articles = response.json().get('articles', [])
        print(f"DEBUG: Found {len(articles)} articles for {keyword}")
        if not articles:
            safe_streamlit_info(f"No recent news found for {keyword}.")
            return 0
        
        scores = []
        for i, article in enumerate(articles[:20]):
            text = article.get('title', '') + " " + article.get('description', '')
            if text.strip():
                result = sentiment_analyzer(text, truncation=True, max_length=512)[0]
                score = result['score'] if result['label'] == 'positive' else -result['score']
                print(f"DEBUG: Article {i+1} sentiment: label={result['label']}, score={result['score']}, mapped_score={score}")
                scores.append(score)
        
        avg_score = np.mean(scores) if scores else 0
        print(f"DEBUG: NewsAPI average sentiment score: {avg_score}")
        return avg_score
    except Exception as e:
        safe_streamlit_error(f"NewsAPI sentiment analysis failed: {str(e)}")
        return 0

@st.cache_data
def get_coingecko_sentiment(coin_id, api_key):
    """
    Fetch coin description from CoinGecko and compute sentiment with FinBERT.
    
    Args:
        coin_id (str): CoinGecko coin ID (e.g., 'bitcoin').
        api_key (str): CoinGecko Demo API key from .env.
    
    Returns:
        float: Sentiment score (-1 to 1), or 0 if no data.
    """
    try:
        sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?x_cg_demo_api_key={api_key}"
        print(f"DEBUG: Fetching CoinGecko URL: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            safe_streamlit_warning(f"CoinGecko request failed for {coin_id} (status {response.status_code}). Response: {response.text}")
            return 0
        
        data = response.json()
        description = data.get('description', {}).get('en', '')
        print(f"DEBUG: CoinGecko description length: {len(description)} characters")
        if not description:
            safe_streamlit_info(f"No description available for {coin_id}.")
            return 0
        
        result = sentiment_analyzer(description, truncation=True, max_length=512)[0]
        score = result['score'] if result['label'] == 'positive' else -result['score']
        print(f"DEBUG: CoinGecko sentiment: label={result['label']}, score={result['score']}, mapped_score={score}")
        return score
    except Exception as e:
        safe_streamlit_error(f"CoinGecko sentiment analysis failed: {str(e)}")
        return 0

def get_sentiment(crypto_name):
    """
    Combine NewsAPI and CoinGecko sentiment scores for the selected cryptocurrency.
    
    Args:
        crypto_name (str): Cryptocurrency name (e.g., 'Bitcoin').
    
    Returns:
        float: Combined sentiment score (-1 to 1), or 0 if analysis fails.
    """
    try:
        load_dotenv()
        newsapi_key = os.getenv("NEWSAPI_KEY")
        coingecko_key = os.getenv("COINGECKO_API_KEY")
        if not newsapi_key or not coingecko_key:
            raise Exception("Missing API keys in .env file (NEWSAPI_KEY or COINGECKO_API_KEY)")
        
        coin_id_mapping = {
            "Bitcoin": "bitcoin",
            "Ethereum": "ethereum",
            "Dogecoin": "dogecoin"
        }
        coin_id = coin_id_mapping.get(crypto_name, "bitcoin")
        
        print(f"DEBUG: Processing sentiment for {crypto_name} (CoinGecko ID: {coin_id})")
        newsapi_score = get_newsapi_sentiment(crypto_name, newsapi_key)
        coingecko_score = get_coingecko_sentiment(coin_id, coingecko_key)
        
        combined_score = 0.6 * newsapi_score + 0.4 * coingecko_score
        print(f"DEBUG: Combined sentiment score: 0.6 * {newsapi_score} + 0.4 * {coingecko_score} = {combined_score}")
        return combined_score
    except Exception as e:
        safe_streamlit_error(f"Sentiment analysis failed: {str(e)}")
        return 0