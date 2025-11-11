#collect data.py
# Reddit (PRAW) Setup
import praw
import pandas as pd
import datetime as dt
import os # import the os module

# ... (rest of your code) ...

# Save to CSV
def collect_reddit_data():
    reddit_data = fetch_reddit()
    
    # Create the 'data' directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    reddit_data.to_csv("data/reddit_data.csv", index=False)
    return reddit_data

# Reddit Keys (Create Reddit app at https://www.reddit.com/prefs/apps)
reddit_keys = {
    "client_id": "Vre8daZqavZiK7GKyEmTSg",
    "client_secret": "xujrqsqhqUbX9b1WzgfM6n3oIdsLdQ",
    "user_agent": "CryptoSentimentBot/0.1 by u/srikar"
}

# Fetch Reddit Posts
def fetch_reddit(subreddit="CryptoCurrency", limit=100):
    reddit = praw.Reddit(
        client_id=reddit_keys["client_id"],
        client_secret=reddit_keys["client_secret"],
        user_agent=reddit_keys["user_agent"]
    )
    posts = reddit.subreddit(subreddit).hot(limit=limit)

    data = [
        {
            "text": post.title + " " + post.selftext,
            "time": dt.datetime.fromtimestamp(post.created_utc),
            "source": "reddit"
        }
        for post in posts if not post.stickied
    ]
    return pd.DataFrame(data)

# Save to CSV
def collect_reddit_data():
    reddit_data = fetch_reddit()
    reddit_data.to_csv("/Users/k.srikar/Desktop/CryptoSense/data/raw_data.csv", index=False)
    return reddit_data

if __name__ == "__main__":
    collect_reddit_data()
