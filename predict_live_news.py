import pandas as pd
import re
import joblib

# STEP 1: Load live news data
df = pd.read_csv("live_news.csv")

# STEP 2: Text cleaning (USE SAME LOGIC AS TRAINING)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

df["clean_text"] = df["text"].apply(clean_text)

# STEP 3: Load model & vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# STEP 4: Vectorize
X = vectorizer.transform(df["clean_text"])

# STEP 5: Predict
df["prediction"] = model.predict(X)

# STEP 6: Confidence score (if supported)
if hasattr(model, "predict_proba"):
    df["credibility"] = model.predict_proba(X).max(axis=1) * 100
else:
    df["credibility"] = "N/A"

# STEP 7: Save results
df.to_csv("live_news_predictions.csv", index=False)

print("Predictions saved to live_news_predictions.csv")
