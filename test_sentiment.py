from sentiment import get_sentiment
try:
    score = get_sentiment("bitcoin")
    print(f"Sentiment score for Bitcoin: {score}")
except Exception as e:
    print(f"Error: {str(e)}")