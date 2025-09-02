import tweepy
import time
import sys
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Custom modules
from pipeline.sentiment import classify_sentiment
from pipeline.preprocess import clean_text
from pipeline.generate_reply import generate_reply
from utils.save_replies import save_reply_to_csv

# Load environment variables from .env
load_dotenv()

# ✅ Initialize Twitter API clients
read_client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN")
)

post_client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

# ✅ Define the query
query = "python lang:en -is:retweet"

# ✅ Fetch recent tweets
print("🔍 Searching tweets...")
response = read_client.search_recent_tweets(query=query, max_results=10)

# ✅ Process each tweet
if response.data:
    for tweet in response.data[:3]:
        print(f"\n📥 Tweet: {tweet.text}")
        try:
            # Step 1: Clean
            cleaned = clean_text(tweet.text)
            print("🧹 Cleaned:", cleaned)

            if not cleaned.strip():
                print("⚠️ Skipping: Cleaned tweet is empty.")
                continue

            # Step 2: Sentiment
            sentiment = classify_sentiment(cleaned)
            print("📊 Sentiment:", sentiment)

            # Step 3: AI-generated reply
            reply = generate_reply(tweet.text, sentiment)
            print("🤖 AI Reply:", reply)

            if not reply or len(reply.strip()) < 2:
                print("⚠️ Skipping: AI Reply is empty or too short.")
                continue

            # Step 4: Save to CSV
            save_reply_to_csv(tweet.text, sentiment, reply)
            print("💾 Saved to CSV")

            # Step 5: Post reply to Twitter (optional - uncomment to enable)
            # post_client.create_tweet(text=reply, in_reply_to_tweet_id=tweet.id)
            # print("✅ Posted reply on Twitter")

            # Step 6: Pause to avoid rate limiting
            time.sleep(5)

        except Exception as e:
            print("❌ Error:", e)
else:
    print("⚠️ No tweets found.")