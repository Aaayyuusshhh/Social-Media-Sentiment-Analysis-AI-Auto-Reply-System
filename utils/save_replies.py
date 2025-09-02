import csv
import os

CSV_FILE = os.path.join("replies", "twitter_replies.csv")

def save_reply_to_csv(comment, sentiment, reply):
    os.makedirs("replies", exist_ok=True)
    with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([comment, sentiment, reply])
