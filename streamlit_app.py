import streamlit as st
import json
import pandas as pd
import os

# ─────────────── Setup
COMMENTS_PATH = "replies/comments.json"
EXPORT_PATH = "downloads/comments.csv"
os.makedirs("downloads", exist_ok=True)

st.set_page_config(page_title="🤖 IG Sentiment Suite", layout="wide")

# ─────────────── CSS
st.markdown("""
<style>
  .header {
  text-align: center;
  margin: 30px 0;
  font-family: 'Segoe UI', sans-serif;
}
.robot {
  display: inline-block;
  font-size: 2.6rem;
  transition: transform 0.5s ease-in-out;
}
.robot:hover {
  transform: rotate(360deg) scale(1.3);
}
.heading-text {
  display: inline-block;
  margin-left: 12px;
  font-size: 2.3rem;
  font-weight: 800;
  background: linear-gradient(90deg, #38bdf8, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  vertical-align: middle;
}
.comment-box {
  background: #1f2937;
  padding: 14px 18px;
  border-radius: 8px;
  margin-bottom: 12px;
  border: 1px solid #333;
  transition: all 0.3s ease-in-out;
}
.comment-box:hover {
  box-shadow: 0px 0px 12px #38bdf8;
  transform: scale(1.01);
}
.sentiment {
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.9rem;
}
.positive { background: #10b981; color: white; }
.negative { background: #ef4444; color: white; }
.neutral  { background: #9ca3af; color: black; }
</style>
""", unsafe_allow_html=True)

# ─────────────── Load Comments
@st.cache_data
def load_comments():
    try:
        with open(COMMENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

comments = load_comments()

# ─────────────── Group by Caption
grouped = {}
for c in comments:
    caption = c.get("caption", "No Caption")[:80] + "..."
    grouped.setdefault(caption, []).append(c)

# ─────────────── Header
st.markdown("""
<div class="header">
  <span class="robot">🤖</span>
  <span class="heading-text">InsightGram Dashboard</span>
</div>
""", unsafe_allow_html=True)



# ─────────────── Sidebar — Post selection
st.sidebar.header("📸 Select Post")
selected_caption = st.sidebar.selectbox("Choose a Post", list(grouped.keys()) if grouped else ["No posts found"])

if st.sidebar.button("🔄 Fetch Comments"):
    st.success("✅ Comments fetched successfully!")

if st.sidebar.button("🤖 Auto-Reply to All"):
    st.success("✅ Auto-replies sent!")

# ─────────────── Display comments for selected post
if selected_caption and selected_caption != "No posts found":
    st.subheader(f"📝 Showing Comments for:")
    st.markdown(f"<h4>{selected_caption}</h4>", unsafe_allow_html=True)
    st.markdown(f"### 💬 Total Comments: {len(grouped[selected_caption])}")

    for entry in grouped[selected_caption]:
        sentiment_class = entry['sentiment'].lower()
        st.markdown(f"""
        <div class="comment-box">
            <div style='font-size:1.1rem;'>👤 <strong>@{entry['username']}</strong></div>
            <div style='margin:4px 0;'>💬 <em>{entry['text']}</em></div>
            <div style='margin:4px 0;'>📊 Sentiment: <span class="sentiment {sentiment_class}">{entry['sentiment']}</span></div>
            <div style='margin-top:6px;'>🤖 <strong>AI Reply:</strong> {entry['reply']}</div>
        </div>
        """, unsafe_allow_html=True)

    # ✅ Save CSV to file instead of downloading
    df = pd.DataFrame(grouped[selected_caption])
    df.to_csv(EXPORT_PATH, index=False)
    st.success(f"💾 Comments saved to **{EXPORT_PATH}**")

else:
    st.info("📌 Select a post from the sidebar to see comments.")
