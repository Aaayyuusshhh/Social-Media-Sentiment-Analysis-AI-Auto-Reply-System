# pipeline/sentiment.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# ─────────────────────────────
# VADER Sentiment Analyzer (used for fast classification)
analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(text):
    """
    Fast rule-based sentiment using VADER.
    Returns: Positive, Negative, or Neutral
    """
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# ─────────────────────────────
# RoBERTa Transformer Model (optional, used if needed)
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

labels = ['Negative', 'Neutral', 'Positive']

def analyze_text(text):
    """
    Deep NLP sentiment using HuggingFace RoBERTa.
    Returns: Positive, Negative, or Neutral
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probs).item()
        return labels[predicted_class]