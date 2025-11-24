from sentiment import safe_streamlit_error, safe_streamlit_info
import numpy as np

def predict_price(informer_input):
    """
    Predict the cryptocurrency price for the given timeframe using a simplified rule-based model.
    
    Args:
        informer_input (dict): Input containing sentiment_score, current_price, timeframe.
    
    Returns:
        float: Predicted price, or None if prediction fails.
    """
    try:
        # Extract sentiment score, default to 0 if missing
        sentiment_score = informer_input.get("sentiment_score", 0)
        # Extract current price, default to 0 if missing
        current_price = informer_input.get("current_price", 0)
        # Extract timeframe, default to '1h' if missing
        timeframe = informer_input.get("timeframe", "1h")
        
        # Check if current price is valid
        if current_price == 0:
            # Log error if price is invalid
            safe_streamlit_error("Invalid current price for prediction.")
            return None
        
        # Map timeframe to hours for scaling the prediction
        timeframe_mapping = {
            "1h": 1,    # 1 hour
            "1d": 24,   # 1 day
            "1w": 168   # 1 week
        }
        # Get time horizon in hours, default to 1 if timeframe is invalid
        time_horizon = timeframe_mapping.get(timeframe, 1)
        
        # Simplified prediction model: adjusts price based on sentiment
        # Formula: predicted_price = current_price * (1 + sentiment_score * volatility_factor * time_horizon)
        volatility_factor = 0.01  # Base volatility: 1% per hour
        price_change_factor = sentiment_score * volatility_factor * time_horizon
        predicted_price = current_price * (1 + price_change_factor)
        
        # Log the predicted price
        safe_streamlit_info(f"Predicted price: {predicted_price:.2f} for timeframe {timeframe}")
        return predicted_price
    except Exception as e:
        # Log any exceptions during prediction
        safe_streamlit_error(f"Price prediction failed: {str(e)}")
        return None

def generate_recommendation(current_price, predicted_price):
    """
    Generate buy/sell/hold recommendation based on predicted price movement.
    
    Args:
        current_price (float): Current cryptocurrency price.
        predicted_price (float): Predicted price for the timeframe.
    
    Returns:
        str: Recommendation ('Buy', 'Sell', 'Hold').
    """
    try:
        # Check if price data is valid
        if predicted_price is None or current_price == 0:
            # Log error if data is invalid
            safe_streamlit_error("Cannot generate recommendation due to invalid price data.")
            return "Hold"
        
        # Calculate percentage change in price
        price_change_pct = ((predicted_price - current_price) / current_price) * 100
        
        # Apply thresholds for recommendation
        if price_change_pct > 2:  # Price increase > 2%
            return "Buy"
        elif price_change_pct < -2:  # Price decrease > 2%
            return "Sell"
        else:  # Price change within ±2%
            return "Hold"
    except Exception as e:
        # Log any exceptions during recommendation
        safe_streamlit_error(f"Recommendation generation failed: {str(e)}")
        return "Hold"

def process_informer_input(informer_input):
    """
    Process the Informer input to predict price and generate recommendation.
    
    Args:
        informer_input (dict): Input containing sentiment_score, current_price, timeframe.
    
    Returns:
        dict: Results containing predicted_price and recommendation, or None if processing fails.
    """
    try:
        # Predict the price using the simplified model
        predicted_price = predict_price(informer_input)
        # Check if prediction was successful
        if predicted_price is None:
            return None
        
        # Get the current price from input
        current_price = informer_input.get("current_price", 0)
        # Generate recommendation based on price movement
        recommendation = generate_recommendation(current_price, predicted_price)
        
        # Create result dictionary
        result = {
            "predicted_price": predicted_price,
            "recommendation": recommendation,
            "timeframe": informer_input.get("timeframe", "1h")
        }
        # Log the result for debugging
        print(f"DEBUG: Informer result: {result}")
        return result
    except Exception as e:
        # Log any exceptions during processing
        safe_streamlit_error(f"Informer processing failed: {str(e)}")
        return None