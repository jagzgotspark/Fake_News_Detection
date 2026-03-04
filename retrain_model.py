import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load Kaggle dataset
kaggle_df = pd.read_csv("kaggle_news.csv")

# Rename columns to standard format
kaggle_df = kaggle_df.rename(columns={
    "title": "text",
    "real": "label"
})
kaggle_df["label"] = kaggle_df["label"].astype(int)


# Keep only required columns
kaggle_df = kaggle_df[["text", "label"]]


# STEP 2: Load live scraped + predicted news
live_df = pd.read_csv("live_news_predictions.csv")

# Convert predictions to labels (example)
live_df["label"] = live_df["prediction"].apply(
    lambda x: 1 if x == "REAL" else 0
)

# STEP 3: Combine datasets
combined_df = pd.concat([
    kaggle_df[["text", "label"]],
    live_df[["text", "label"]]
])

# STEP 4: Clean text (SAME as before)
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

combined_df["clean_text"] = combined_df["text"].apply(clean_text)

# STEP 5: Vectorize
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
X = vectorizer.fit_transform(combined_df["clean_text"])
y = combined_df["label"]

# STEP 6: Retrain model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# STEP 7: Save updated model
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model retrained and updated successfully")
