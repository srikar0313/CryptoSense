from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()

def apply_sentiment(df):
    df["sentiment"] = df["text"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
    return df

if __name__ == "__main__":
    raw = pd.read_csv("data/raw_data.csv")
    scored = apply_sentiment(raw)
    print(scored.head())
