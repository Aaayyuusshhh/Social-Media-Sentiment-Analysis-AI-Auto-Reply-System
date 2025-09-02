import os
import requests
import json
from pipeline.sentiment import analyze_text
from pipeline.generate_reply import generate_reply

class InstagramBot:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.ig_user_id = os.getenv("IG_USER_ID")

        # Track already replied comment IDs
        self.processed_path = "data/processed_instagram_comments.json"
        self.processed_comments = self._load_processed_comments()

    def _load_processed_comments(self):
        try:
            with open(self.processed_path, "r") as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def _save_processed_comments(self):
        os.makedirs("data", exist_ok=True)
        with open(self.processed_path, "w") as f:
            json.dump(list(self.processed_comments), f)

    def fetch_comments(self, limit=5):
        """Fetch latest comments on recent posts from business IG account"""
        media_url = f"https://graph.facebook.com/v19.0/{self.ig_user_id}/media?fields=id,caption&limit={limit}&access_token={self.access_token}"
        media_res = requests.get(media_url).json()

        if "data" not in media_res:
            print("❌ No media found or token is invalid")
            return []

        all_comments = []

        for media in media_res["data"]:
            media_id = media.get("id")
            caption = media.get("caption", "No caption")

            comments_url = f"https://graph.facebook.com/v19.0/{media_id}/comments?fields=id,text,username&access_token={self.access_token}"
            comments_res = requests.get(comments_url).json()

            comments = comments_res.get("data", [])
            for comment in comments:
                if comment["id"] not in self.processed_comments:
                    all_comments.append({
                        "comment_id": comment["id"],
                        "username": comment.get("username", "unknown"),
                        "text": comment.get("text", ""),
                        "media_id": media_id,
                        "caption": caption
                    })

        return all_comments

    def reply_to_comment(self, comment_id, message):
        """Replies to a comment on Instagram"""
        reply_url = f"https://graph.facebook.com/v19.0/{comment_id}/replies"
        response = requests.post(reply_url, params={
            "message": message,
            "access_token": self.access_token
        })

        if response.status_code == 200:
            self.processed_comments.add(comment_id)
            self._save_processed_comments()
            return True
        else:
            print(f"[❌] Failed to reply: {response.text}")
            return False

    def process_comments(self):
        """Main pipeline: fetch → analyze → generate reply → respond → save"""
        comments = self.fetch_comments()
        print(f"📥 {len(comments)} new comments to process.")
        results = []

        for comment in comments:
            try:
                text = comment["text"]
                sentiment = analyze_text(text)
                reply = generate_reply(text, sentiment)

                print(f"🤖 @{comment['username']} said: {text}")
                print(f"🧠 Sentiment: {sentiment} → Reply: {reply}")

                success = self.reply_to_comment(comment["comment_id"], reply)
                if success:
                    result_entry = {
                        "username": comment["username"],
                        "text": text,
                        "caption": comment["caption"],
                        "media_id": comment["media_id"],
                        "sentiment": sentiment,
                        "reply": reply
                    }
                    results.append(result_entry)

            except Exception as e:
                print(f"[⚠️] Error processing comment {comment.get('comment_id')}: {str(e)}")

        # Save full results to JSON
        if results:
            os.makedirs("replies", exist_ok=True)
            with open("replies/comments.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)

        return results
