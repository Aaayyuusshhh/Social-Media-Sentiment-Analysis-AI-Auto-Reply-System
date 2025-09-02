# pipeline/train_model.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from pipeline.preprocess import clean_text

# Load your dataset
df = pd.read_csv('data/sentimentdataset.csv')

# Preprocess text
df['clean_text'] = df['Text'].apply(clean_text)

# Encode sentiment labels
label_encoder = LabelEncoder()
df['encoded_sentiment'] = label_encoder.fit_transform(df['Sentiment'])

# TF-IDF vectorization
tfidf = TfidfVectorizer(max_features=5000)
X = tfidf.fit_transform(df['clean_text'])
y = df['encoded_sentiment']

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save models to models/
joblib.dump(model, 'models/rf_model.pkl')
joblib.dump(tfidf, 'models/tfidf.pkl')
joblib.dump(label_encoder, 'models/label_encoder.pkl')

print("✅ Models saved to models/ folder")
