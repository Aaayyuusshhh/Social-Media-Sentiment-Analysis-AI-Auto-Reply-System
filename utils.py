# utils.py (for Streamlit dashboard, NOT related to utils/save_replies.py)
def mock_sentiment(text):
    if any(word in text.lower() for word in ["not", "don’t", "hate", "bad", "dislike"]):
        return "Negative"
    return "Positive"

def mock_ai_reply(text, sentiment):
    if sentiment == "Positive":
        return "Thank you for your kind words!"
    if "prefer" in text or "work" in text:
        return "We’re sorry to hear that. Let us know how we can improve."
    if "like your work" in text:
        return "We appreciate your feedback and will strive to do better."
    return "Thank you for your feedback."

def analyze_comments(comments):
    analyzed = []
    for comment in comments:
        sentiment = mock_sentiment(comment["text"])
        reply = mock_ai_reply(comment["text"], sentiment)
        analyzed.append({
            **comment,
            "sentiment": sentiment,
            "ai_reply": reply
        })
    return analyzed
