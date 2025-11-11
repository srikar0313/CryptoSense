import pandas as pd
from fetch_price import fetch_price_history
from sentiment import apply_sentiment

def create_features():
    text_df = pd.read_csv("data/raw_data.csv", parse_dates=["time"])
    text_df = apply_sentiment(text_df)
    text_df = text_df.resample("H", on="time").mean().dropna()

    price_df = fetch_price_history()
    combined = text_df.join(price_df, how="inner")

    # Label for next price direction
    combined["future_price"] = combined["price"].shift(-1)
    combined["label"] = (combined["future_price"] > combined["price"]).astype(int)
    combined.drop(columns=["future_price"], inplace=True)

    combined.to_csv("data/feature_data.csv")
    return combined

if __name__ == "__main__":
    df = create_features()
    print(df.head())
