import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_model():
    df = pd.read_csv("data/feature_data.csv")
    X = df[["sentiment", "price"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    joblib.dump(model, "model/random_forest.pkl")
    print(f"Accuracy: {model.score(X_test, y_test):.2f}")

if __name__ == "__main__":
    train_model()
