import streamlit as st
import pandas as pd
import random
import time
import re
from datetime import datetime
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

SAMPLE_TEXTS = [
    "I absolutely love this product, it's amazing!",
    "This is the worst experience I've ever had.",
    "The service was okay, nothing special.",
    "Best customer support ever, so helpful and responsive!",
    "Terrible quality, product arrived damaged.",
    "Pretty happy with my purchase overall.",
    "Awful, buggy app that keeps crashing.",
    "Excellent value for the price, highly recommend.",
    "I am disappointed, it broke after one use.",
    "Great experience, will buy again!",
    "Horrible customer service, declined my refund.",
    "Wonderful design and perfect performance.",
]

def get_sentiment(text):
    positive_words = ['love', 'amazing', 'wonderful', 'excellent', 'best', 'great', 'happy', 'excited', 'helpful', 'responsive', 'perfect']
    negative_words = ['worst', 'hate', 'terrible', 'disappointed', 'bad', 'awful', 'horrible', 'poor', 'damaged', 'buggy', 'declined']
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    if pos_count > neg_count:
        return 'POSITIVE', random.uniform(0.75, 0.95)
    elif neg_count > pos_count:
        return 'NEGATIVE', random.uniform(0.75, 0.95)
    else:
        return 'NEUTRAL', random.uniform(0.50, 0.70)

def generate_data():
    text = random.choice(SAMPLE_TEXTS)
    sentiment, confidence = get_sentiment(text)
    return {
        'timestamp': datetime.now(),
        'text': text,
        'sentiment': sentiment,
        'confidence': confidence,
        'platform': random.choice(['Twitter', 'Reddit', 'Facebook']),
        'location': random.choice(['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Berlin', 'Moscow'])
    }

st.set_page_config(page_title="Sentiment Analysis Dashboard", page_icon="📊", layout="wide")
st.title("📊 Real-Time Sentiment Analysis Dashboard")
st.markdown("---")

if 'data' not in st.session_state:
    st.session_state.data = []

st.sidebar.header("🎛️ Controls")
if st.sidebar.button("🔄 Generate New Data"):
    st.session_state.data.append(generate_data())
    if len(st.session_state.data) > 100:
        st.session_state.data = st.session_state.data[-100:]

auto_generate = st.sidebar.checkbox("Auto Generate", value=True)
if st.sidebar.button("🗑️ Clear All Data"):
    st.session_state.data = []
st.sidebar.markdown("---")
st.sidebar.info(f"📊 Total Data Points: {len(st.session_state.data)}")

if auto_generate and len(st.session_state.data) < 100:
    st.session_state.data.append(generate_data())
    time.sleep(0.5)
    st.rerun()

df = pd.DataFrame(st.session_state.data)

if not df.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📝 Total Posts", len(df))
    with col2:
        positive_pct = (df['sentiment'] == 'POSITIVE').sum() / len(df) * 100
        st.metric("😊 Positive", f"{positive_pct:.1f}%")
    with col3:
        negative_pct = (df['sentiment'] == 'NEGATIVE').sum() / len(df) * 100
        st.metric("😞 Negative", f"{negative_pct:.1f}%")
    with col4:
        neutral_pct = (df['sentiment'] == 'NEUTRAL').sum() / len(df) * 100
        st.metric("😐 Neutral", f"{neutral_pct:.1f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        sentiment_counts = df['sentiment'].value_counts()
        colors = {'POSITIVE': '#00cc66', 'NEUTRAL': '#ffcc00', 'NEGATIVE': '#ff3333'}
        color_list = [colors.get(s, '#808080') for s in sentiment_counts.index]
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=.4,
            marker=dict(colors=color_list),
            textinfo='label+percent',
            textposition='auto'
        )])
        fig.update_layout(title='Sentiment Distribution', height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if 'platform' in df.columns:
            platform_counts = df['platform'].value_counts()
            platform_colors = {'Twitter': '#1DA1F2', 'Reddit': '#FF4500', 'Facebook': '#4267B2'}
            platform_color_list = [platform_colors.get(p, '#808080') for p in platform_counts.index]
            fig = go.Figure(data=[go.Bar(
                x=platform_counts.index,
                y=platform_counts.values,
                marker_color=platform_color_list,
                text=platform_counts.values,
                textposition='auto'
            )])
            fig.update_layout(title='Posts by Platform', height=400, xaxis_title='Platform', yaxis_title='Count')
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("☁️ Word Cloud")
    all_text = ' '.join(df['text'].values)
    all_text = re.sub(r'[^\w\s]', '', all_text.lower())
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis', max_words=100).generate(all_text)
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    except Exception:
        st.warning("Not enough text for word cloud")

    st.markdown("---")
    st.subheader("📋 Recent Posts")
    recent_df = df.tail(10).iloc[::-1]
    for _, row in recent_df.iterrows():
        color = {'POSITIVE': '#00cc66', 'NEUTRAL': '#ffcc00', 'NEGATIVE': '#ff3333'}.get(row['sentiment'], '#808080')
        emoji = {'POSITIVE': '😊', 'NEUTRAL': '😐', 'NEGATIVE': '😞'}.get(row['sentiment'], '')
        st.markdown(f"""
        <div style="border-left: 5px solid {color}; padding: 10px; margin: 5px 0; background-color: #f8f9fa; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 16px; color: #333;">{row['text']}</span>
                <span style="font-weight: bold; color: {color};">{emoji} {row['sentiment']}</span>
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 5px;">
                Confidence: {row['confidence']:.2%} | Platform: {row.get('platform', 'Unknown')} | {row['timestamp'].strftime('%H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Confidence", f"{df['confidence'].mean():.2%}")
    with col2:
        most_common = df['platform'].mode().iloc[0] if not df['platform'].empty else "N/A"
        st.metric("Most Active Platform", most_common)
    with col3:
        st.metric("Total Posts Analyzed", len(df))
else:
    st.info("📊 No data yet. Click 'Generate New Data' or enable 'Auto Generate' to start!")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #666; font-size: 12px;">Real-Time Sentiment Analysis Dashboard | Data updates in real-time</div>', unsafe_allow_html=True)
