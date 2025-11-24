
# CryptoSense

CryptoSense is a cryptocurrency analytics and prediction application that combines real-time data collection, sentiment analysis, and forecasting using the Informer model.

## 📂 Project Structure

```
cryptosense/
│
├── app.py                  # Main application runner
├── binance_data.py         # Fetches and processes data from Binance API
├── informer_model.py       # Informer model for time series forecasting
├── sentiment.py            # Sentiment analysis from news or social media
├── test_informer.py        # Unit tests for Informer model
├── test_sentiment.py       # Unit tests for sentiment analysis
├── crypto_logo.png         # Project logo
├── .env                    # Environment variables (API keys, etc.)
└── __pycache__/            # Python bytecode cache
```

## 🚀 Features

- Live cryptocurrency data fetching from Binance
- Sentiment analysis from news or tweets
- Time-series forecasting using Informer model
- CLI or backend API driven analysis
- Modular architecture and test coverage

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cryptosense.git
   cd cryptosense
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API keys**
   - Create a `.env` file with necessary keys, e.g.:
     ```env
     BINANCE_API_KEY=your_key_here
     NEWS_API_KEY=your_key_here
     ```

5. **Run the application**
   ```bash
   python app.py
   ```

## ✅ Testing

```bash
python test_informer.py
python test_sentiment.py
```

## 📈 Dependencies

Include in `requirements.txt` (if not already):
- `pandas`
- `numpy`
- `requests`
- `matplotlib`
- `transformers`
- `scikit-learn`
- `python-dotenv`

## 📄 License

MIT License. See `LICENSE` for details.

## ✨ Acknowledgments

- Binance for live market data
- HuggingFace Transformers for sentiment analysis models
- Authors of the Informer architecture
