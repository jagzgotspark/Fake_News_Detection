import joblib
import pandas as pd
import numpy as np
import re

import pickle


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

from nltk.stem import PorterStemmer

# Hardcoded English stopwords (Streamlit-safe)
stop_words = {
    'a','an','the','and','or','but','if','while','with','without','of','at','by',
    'for','to','from','in','on','is','are','was','were','be','been','being',
    'this','that','these','those','it','its','as','about','into','than','then',
    'so','such','too','very','can','will','just','not'
}

ps = PorterStemmer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub('[^a-z]', ' ', text)
    words = text.split()
    words = [ps.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

df = pd.read_csv("fake_news.csv")
print("COLUMNS IN DATASET:")
print(df.columns)


# Load dataset
df = pd.read_csv("fake_news.csv")

# Use correct columns from your dataset
TEXT_COL = 'title'
LABEL_COL = 'real'

# Keep only required columns
df = df[[TEXT_COL, LABEL_COL]]

# Rename for consistency
df.columns = ['text', 'label']

# Apply cleaning
df['clean_text'] = df['text'].apply(clean_text)

# Features and labels
X = df['clean_text']
y = df['label']


vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy * 100)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model and Vectorizer saved successfully")

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model and vectorizer saved successfully")
