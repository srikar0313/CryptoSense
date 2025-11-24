import requests
from sentiment import get_sentiment, safe_streamlit_error, safe_streamlit_warning

def get_binance_price(symbol):
    """
    Fetch the current price of a cryptocurrency from Binance's public API.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT' for Bitcoin).
    
    Returns:
        float: Current price in USDT, or None if the request fails.
    """
    try:
        # Construct the Binance API URL for the ticker price endpoint
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        # Make the HTTP GET request to Binance
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            # Log error if the API request fails
            safe_streamlit_error(f"Binance API request failed (status {response.status_code}).")
            return None
        # Parse the JSON response to extract the price
        data = response.json()
        price = float(data.get('price', 0))
        # Check if a valid price was returned
        if price == 0:
            # Log warning if no price data is available
            safe_streamlit_warning(f"No price data available for {symbol}.")
            return None
        return price
    except Exception as e:
        # Log any exceptions during the request or parsing
        safe_streamlit_error(f"Binance price fetch failed: {str(e)}")
        return None

def prepare_informer_input(crypto_name, timeframe):
    """
    Prepare input for the Informer model by combining sentiment score and current price.
    
    Args:
        crypto_name (str): Cryptocurrency name (e.g., 'Bitcoin').
        timeframe (str): Prediction timeframe (e.g., '1h', '1d', '1w').
    
    Returns:
        dict: Input data for Informer with sentiment_score, current_price, timeframe, or None if data fetching fails.
    """
    try:
        # Define mapping of cryptocurrency names to Binance trading pair symbols
        symbol_mapping = {
            "Bitcoin": "BTCUSDT",
            "Ethereum": "ETHUSDT",
            "Dogecoin": "DOGEUSDT"
        }
        # Get the Binance symbol for the given cryptocurrency, default to BTCUSDT
        symbol = symbol_mapping.get(crypto_name, "BTCUSDT")
        # Get the sentiment score from sentiment.py
        sentiment_score = get_sentiment(crypto_name)
        # Fetch the current price from Binance
        current_price = get_binance_price(symbol)
        # Check if price fetching was successful
        if current_price is None:
            # Log error if price fetch failed
            safe_streamlit_error("Failed to fetch current price. Cannot prepare Informer input.")
            return None
        # Create the input dictionary for the Informer model
        informer_input = {
            "sentiment_score": sentiment_score,
            "current_price": current_price,
            "timeframe": timeframe
        }
        # Log the prepared input for debugging
        print(f"DEBUG: Informer input prepared: {informer_input}")
        return informer_input
    except Exception as e:
        # Log any exceptions during input preparation
        safe_streamlit_error(f"Failed to prepare Informer input: {str(e)}")
        return None