import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Social Media Analytics - India",
                   layout="wide")

st.markdown("""
    <style>
        .metric-card {
            background-color: #1e1e2f;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
        }
        .title-text {
            font-size: 32px;
            font-weight: bold;
            color: #00d4ff;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== LOAD DATA =====================
df = pd.read_csv("../data/processed/reviews_sentiment_small.csv")
df_clean = pd.read_csv("../data/processed/reviews_cleaned.csv")

platforms = df["Platform"].unique()
selected_platforms = st.sidebar.multiselect("Select Platform", platforms, default=list(platforms))

df = df[df["Platform"].isin(selected_platforms)]
df_clean = df_clean[df_clean["Platform"].isin(selected_platforms)]

# ===================== KPI CARDS =====================
total_reviews = len(df_clean)
avg_rating = round(df_clean["score"].mean(), 2)
avg_sentiment = round(df["sentiment"].mean(), 3)

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class='metric-card'>
Total Reviews<br><span style='font-size:28px;'>{total_reviews:,}</span>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class='metric-card'>
Avg Rating ⭐<br><span style='font-size:28px;'>{avg_rating}</span>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class='metric-card'>
Avg Sentiment 😊<br><span style='font-size:28px;'>{avg_sentiment}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='title-text'>📊 Platform Analytics Dashboard</p>", unsafe_allow_html=True)

# ===================== RATING DISTRIBUTION =====================
fig1 = px.histogram(df_clean,
                    x="score",
                    color="Platform",
                    barmode="group",
                    title="⭐ Rating Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set2)

fig1.update_layout(
    template="plotly_dark",
    plot_bgcolor="#111218",
    paper_bgcolor="#111218",
    font_color="white"
)
st.plotly_chart(fig1, use_container_width=True)

# ===================== SENTIMENT COMPARISON =====================
fig2 = px.box(df,
              x="Platform",
              y="sentiment",
              title="😊 Sentiment Comparison",
              color="Platform",
              color_discrete_sequence=px.colors.qualitative.Set1)

fig2.update_layout(template="plotly_dark",
                   plot_bgcolor="#111218",
                   paper_bgcolor="#111218",
                   font_color="white")
st.plotly_chart(fig2, use_container_width=True)

# ===================== TREND OF REVIEWS =====================
# =========================
# 📈 Review Trends (Daily)
# =========================
st.subheader("📈 Review Trend Over Time (Daily Count)")

df_time = df_clean.copy()
df_time["Day"] = pd.to_datetime(df_time["at"]).dt.date

trend = df_time.groupby(["Day", "Platform"]).size().reset_index(name="Review Count")

fig_count = px.line(
    trend,
    x="Day",
    y="Review Count",
    color="Platform",
    markers=True,
    title="Daily Review Count Trend",
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig_count.update_layout(
    template="plotly_dark",
    plot_bgcolor="#111218",
    paper_bgcolor="#111218",
    font_color="white"
)

st.plotly_chart(fig_count, use_container_width=True)


# =======================================
# 📊 Normalized Trend (%) Comparison
# =======================================
st.subheader("📊 Platform Popularity Share (%) Over Time")

trend["PctShare"] = trend.groupby("Day")["Review Count"].transform(lambda x: (x / x.sum()) * 100)

fig_pct = px.line(
    trend,
    x="Day",
    y="PctShare",
    color="Platform",
    markers=True,
    title="Daily Market Share of Reviews (%)",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_pct.update_layout(
    template="plotly_dark",
    plot_bgcolor="#111218",
    paper_bgcolor="#111218",
    font_color="white",
    yaxis_title="Share (%)"
)

st.plotly_chart(fig_pct, use_container_width=True)


# Insight message for your viva
st.info("""
📌 Insight: Facebook reviews come mostly in bursts (update-related),
while Snapchat & Twitter show consistent day-to-day activity.
Normalized % share helps compare platform popularity fairly.
""")



from prophet import Prophet

st.subheader("🔮 Future Popularity Forecast (Next 30 Days)")

forecast_platform = st.selectbox("Select Platform for Forecast:", selected_platforms)

df_forecast = df_time[df_time["Platform"] == forecast_platform][["Day"]].copy()
df_forecast.rename(columns={"Day": "ds"}, inplace=True)
df_forecast["y"] = 1  # Count per day

df_forecast = df_forecast.groupby("ds").size().reset_index(name="y")

model = Prophet()
model.fit(df_forecast)

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

fig4 = px.line(forecast,
               x="ds",
               y="yhat",
               title=f"Popularity Forecast → {forecast_platform}")

fig4.update_layout(template="plotly_dark",
                   plot_bgcolor="#111218",
                   paper_bgcolor="#111218",
                   font_color="white")

st.plotly_chart(fig4, use_container_width=True)
st.info("""
🔮 Insight: Since the dataset contains only very recent reviews from the same day,
Prophet predicts a decline — indicating data is collected at a peak activity moment.
More historical data would show actual seasonal growth trends.
""")



st.subheader("🎯 User Engagement Insights")

# Group by ratings to see loyalty breakdown
engagement_df = df_clean.groupby("score")["thumbsUpCount"].mean().reset_index()

fig_eng = px.bar(engagement_df,
                 x="score",
                 y="thumbsUpCount",
                 title="Avg Engagement by Rating Score",
                 color="score",
                 color_discrete_sequence=px.colors.sequential.Viridis)

fig_eng.update_layout(template="plotly_dark",
                      plot_bgcolor="#111218",
                      paper_bgcolor="#111218",
                      font_color="white")

st.plotly_chart(fig_eng, use_container_width=True)
st.info("""
🎯 Insight: 1-star reviews get the highest engagement 📢  
Users with negative experiences tend to write detailed reviews and react to others.
This helps platforms identify critical improvement areas.
""")


