from flask import Flask, request, jsonify
from pipeline.sentiment import analyze_text
from pipeline.generate_reply import generate_reply
from instagram_bot import InstagramBot
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
instagram_bot = InstagramBot()

# ✅ Global environment variables
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "your_default_token_here")

# ----------------------- Core Endpoints -----------------------

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    sentiment = analyze_text(text)
    reply = generate_reply(text, sentiment)
    return jsonify({'sentiment': sentiment, 'reply': reply})


@app.route('/process_instagram', methods=['GET', 'POST'])
def process_instagram():
    try:
        # Step 1: Fetch IG comments
        print("📡 Fetching Instagram comments...")
        comments = instagram_bot.fetch_comments()
        print(f"✅ {len(comments)} comments fetched")

        final_data = []

        for comment in comments:
            text = comment["text"]
            sentiment = analyze_text(text)
            reply = generate_reply(text, sentiment)

            entry = {
                "username": comment["username"],
                "text": text,
                "caption": comment["caption"],
                "media_id": comment["media_id"],
                "sentiment": sentiment,
                "reply": reply
            }
            final_data.append(entry)

        # Step 2: Save to replies/comments.json
        os.makedirs("replies", exist_ok=True)
        with open("replies/comments.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2)

        print("💾 Saved to replies/comments.json")
        return jsonify({'status': 'success', 'processed': final_data}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/ping')
def ping():
    return "Localhost is working!", 200


@app.route('/test_instagram')
def test_ig():
    try:
        url = f"https://graph.instagram.com/me?fields=id,username&access_token={ACCESS_TOKEN}"
        response = requests.get(url)
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/debug')
def debug():
    return jsonify({
        "flask_running": True,
        "instagram_connected": bool(ACCESS_TOKEN),
        "mode": "development"
    })


@app.route('/get_ig_id')
def get_ig_id():
    page_url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={ACCESS_TOKEN}"
    page_res = requests.get(page_url).json()

    if 'data' not in page_res or not page_res['data']:
        return jsonify({'error': 'No pages found or token invalid', 'response': page_res}), 400

    page_id = page_res['data'][0]['id']
    ig_url = f"https://graph.facebook.com/v19.0/{page_id}?fields=instagram_business_account&access_token={ACCESS_TOKEN}"
    ig_res = requests.get(ig_url).json()

    return jsonify({
        "page_id": page_id,
        "ig_user_id": ig_res.get('instagram_business_account', {}).get('id'),
        "raw_response": ig_res
    })


@app.route('/get_ig_comments')
def get_ig_comments():
    print("DEBUG IG_USER_ID:", IG_USER_ID)
    print("DEBUG ACCESS_TOKEN:", ACCESS_TOKEN[:20] + "..." if ACCESS_TOKEN else None)

    media_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media?fields=id,caption&limit=10&access_token={ACCESS_TOKEN}"
    media_res = requests.get(media_url).json()
    print("MEDIA RES:", media_res)

    flat_comments = []

    if 'data' not in media_res:
        return jsonify({'error': 'No media found or token is invalid', 'response': media_res}), 400

    for media in media_res["data"]:
        media_id = media.get("id")
        caption = media.get("caption", "No caption")

        comments_url = f"https://graph.facebook.com/v19.0/{media_id}/comments?fields=id,text,username&access_token={ACCESS_TOKEN}"
        comments_res = requests.get(comments_url).json()
        print(f"COMMENTS FOR {media_id}:", comments_res)

        comments = comments_res.get("data", [])
        for comment in comments:
            flat_comments.append({
                "media_id": media_id,
                "caption": caption,
                "username": comment.get("username", "unknown"),
                "text": comment.get("text", "")
            })

    print("TOTAL COMMENTS FETCHED:", len(flat_comments))
    return jsonify({"comments": flat_comments})

# ----------------------- Webhook (Meta Verification) -----------------------

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "❌ Verification token mismatch", 403

    elif request.method == 'POST':
        data = request.json
        print("📥 Incoming webhook payload:", data)
        return "EVENT_RECEIVED", 200

# ----------------------- Run Flask App -----------------------

if __name__ == '__main__':
    app.run(port=5000)
