import requests
import pandas as pd

def fetch_price_history(coin_id='bitcoin', vs_currency='usd', days='30'):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days, "interval": "hourly"}
    res = requests.get(url, params=params)
    data = res.json()

    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["time"] = pd.to_datetime(prices["timestamp"], unit="ms")
    prices.set_index("time", inplace=True)
    return prices[["price"]]

if __name__ == "__main__":
    df = fetch_price_history()
    print(df.head())
