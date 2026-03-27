# 🌐 Social Media Sentiment Analysis & AI Auto-Reply System  

Real-time NLP system for sentiment classification and automated responses on social media.  
End-to-end pipeline integrating APIs, transformer models, and LLM-driven replies.   
---

## 🚀 Overview  

- Fine-tuned a transformer-based sentiment classifier on **5K+ social media comments**  
- Deployed a **real-time inference pipeline** using Meta APIs for Instagram and Facebook  
- Built an **end-to-end automation system** from data ingestion → sentiment classification → AI-generated replies  
- Implemented in a **real client-facing workflow**, eliminating manual response effort entirely  
---

## ✨ Features  

### 🧠 Sentiment Intelligence Engine  
- Multi-class sentiment classification: positive, negative, neutral  
- Robust handling of noisy, short-form social media text  
- Optimized transformer pipeline for real-time inference  

### 🤖 Autonomous Reply Generation  
- Context-aware replies generated using LLMs  
- Maintains conversational relevance and tone consistency  
- Designed to simulate human-like brand responses at scale  

### ⚡ End-to-End Automation Pipeline  
- Automated ingestion of comments via **Meta Graph API**  
- Real-time processing and triggering of reply generation  
- Fully eliminates manual monitoring and response effort  

### 🔒 Brand Safety & Control  
- Rule-based filtering layer to enforce safe and controlled outputs  
- Prevents harmful or off-tone responses in production scenarios  

### 📊 Monitoring & Analytics  
- Streamlit dashboard for sentiment tracking and engagement insights  
- Real-time visibility into system activity and model behavior  

---

## 🏗️ Project Structure  

```bash
social_sentiment_ai/
│── requirements.txt
│── README.md
│── .env
│── main.py
│
├── sentiment_analysis/
│   ├── preprocess.py
│   ├── sentiment_model.py
│   ├── sarcasm_model.py
│   ├── explain.py
│
├── auto_reply/
│   ├── reply_generator.py
│   ├── brand_guard.py
│   ├── api.py
│
├── social_media_connectors/
│   ├── instagram_api.py
│   ├── facebook_api.py
│   ├── twitter_api.py
│   ├── youtube_api.py
│
├── dashboard/
│   ├── dashboard.py
│   ├── plots.py
│
├── utils/
│   ├── logger.py
│   ├── config.py
│   ├── helpers.py
│
└── tests/
    ├── test_sentiment.py
    ├── test_auto_reply.py
    ├── test_connectors.py

```
## 🚀 Getting Started
1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/AI-Sentiment-AutoReply.git
cd AI-Sentiment-AutoReply
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Run Flask Backend
```bash
python src/app.py
```
4️⃣ Launch Analytics Dashboard
```bash
streamlit run dashboard/app.py
```
## 🔧 Tech Stack  

The system is built on a **modular AI + backend architecture** designed for real-time inference, automation, and scalability.

### Core Technologies  
- **Python** – Primary language for ML pipelines, backend services, and automation workflows  
- **Flask** – Lightweight REST API layer for serving sentiment predictions and triggering reply generation  
- **Streamlit** – Interactive dashboard for real-time monitoring and analytics  

### Machine Learning & NLP  
- **PyTorch** – Model training and inference  
- **Hugging Face Transformers** – Transformer-based models for contextual sentiment classification  
- **Scikit-learn** – Supporting ML utilities and baseline experimentation  

### LLM & Automation  
- **OpenAI API** – Context-aware reply generation  
- **Prompt Engineering** – Controlled response generation aligned with tone and context  
- **API-driven Workflow Automation** – Integration of ML outputs into real-time response pipelines  

### Data & Processing  
- **Pandas** – Data manipulation and preprocessing  
- **NumPy** – Efficient numerical computation  

### Integrations  
- **Meta Graph API** – Real-time ingestion of Instagram and Facebook comments  

### Deployment & Environment  
- **Docker (optional)** – Containerized deployment for reproducibility  
- **Cloud-ready architecture** – Deployable on platforms like AWS, GCP, or Streamlit Cloud  

---

## 📈 Impact  

- Designed and deployed a **real-time sentiment analysis and response system** for social media workflows  
- Eliminated manual reply processes through **end-to-end automation pipelines**  
- Demonstrated integration of **ML models, APIs, and LLMs in a production-style system**  

---

## 🤝 Contributing  

Contributions are welcome. Feel free to open issues or submit pull requests for improvements.

---

## 📜 License  

This project is licensed under the [MIT License](./LICENSE).
