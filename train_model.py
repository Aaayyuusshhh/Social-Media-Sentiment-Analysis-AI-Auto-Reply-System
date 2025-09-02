import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
from pipeline.preprocess import clean_text
from pipeline.sentiment import polarity_map

df = pd.read_csv('data/sentimentdataset.csv')
df['Clean_Text'] = df['Text'].apply(clean_text)
df['Polarity'] = df['Sentiment'].apply(polarity_map)
df = df.dropna(subset=['Polarity'])

tfidf = TfidfVectorizer(max_features=3000)
X = tfidf.fit_transform(df['Clean_Text'])

le = LabelEncoder()
y = le.fit_transform(df['Polarity'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

joblib.dump(rf_model, 'models/rf_model.pkl')
joblib.dump(tfidf, 'models/tfidf.pkl')
joblib.dump(le, 'models/label_encoder.pkl')
print("Model training complete.")