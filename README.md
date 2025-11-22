# 📊 Social Media App Analytics (India) — Big Data Project

This dashboard analyzes 200,000 recent Google Play reviews from
4 major platforms:

- **Facebook**
- **Instagram**
- **Snapchat**
- **Twitter**

### 🔍 Features

✔ Sentiment Analysis (TextBlob)  
✔ Rating Distribution Comparison  
✔ Daily Trend Visualization  
✔ Market Share (%) Timeline  
✔ User Engagement Metrics  
✔ Popularity Forecasting (Prophet Model)  
✔ Fully Interactive Streamlit Dashboard  

### 🧠 Insights (India Market)

- Snapchat shows **more consistent daily activity**
- Facebook reviews come in **spikes due to update releases**
- Twitter has **medium engagement** but high negative commentary
- 1-Star reviews receive **the highest engagement**

### 🛠️ Tech Stack

| Component | Choice |
|----------|--------|
| Language | Python |
| Dashboard | Streamlit |
| Viz Library | Plotly |
| Forecasting | Facebook Prophet |
| Database | (CSV Big Data Processing) |

### 🚀 Run Locally

```bash
git clone https://github.com/<your-username>/BDA-SocialMedia-Analytics.git
cd BDA-SocialMedia-Analytics
pip install -r requirements.txt
streamlit run dashboard/app.py
