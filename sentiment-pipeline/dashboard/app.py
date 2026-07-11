import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pymongo
import redis
import json
import re
from typing import Optional, List, Dict, Any

from .config import dashboard_config

# Page configuration
st.set_page_config(
    page_title="Real-Time Sentiment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SentimentDashboard:
    """Main dashboard class for sentiment visualization"""
    
    def __init__(self):
        self.db = None
        self.redis_client = None
        self.setup_database()
        self.setup_redis()
        
        # Initialize session state
        if 'last_update' not in st.session_state:
            st.session_state.last_update = datetime.utcnow()
            st.session_state.data = pd.DataFrame()
    
    def setup_database(self):
        """Initialize MongoDB connection"""
        try:
            client = pymongo.MongoClient(dashboard_config.MONGO_URI)
            self.db = client[dashboard_config.MONGO_DATABASE]
        except Exception as e:
            st.warning(f"MongoDB connection: {e}")
            self.db = None
    
    def setup_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis.from_url(
                dashboard_config.REDIS_URL,
                decode_responses=True
            )
            self.redis_client.ping()
        except Exception:
            self.redis_client = None
    
    def get_latest_data(self, limit: int = 1000) -> pd.DataFrame:
        """Fetch latest data from MongoDB"""
        if not self.db:
            return pd.DataFrame()
        
        try:
            collection = self.db[dashboard_config.MONGO_COLLECTION]
            data = list(collection.find(
                {},
                {'_id': 0}
            ).sort('timestamp', -1).limit(limit))
            
            if data:
                df = pd.DataFrame(data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def get_aggregated_stats(self) -> Optional[Dict]:
        """Get aggregated statistics from Redis"""
        if not self.redis_client:
            return None
        
        try:
            stats = self.redis_client.get('sentiment_stats')
            if stats:
                return json.loads(stats)
            return None
        except Exception:
            return None
    
    def create_sentiment_gauge(self, df: pd.DataFrame) -> Optional[go.Figure]:
        """Create sentiment gauge chart"""
        if df.empty:
            return None
        
        sentiment_counts = df['sentiment'].value_counts()
        total = len(df)
        
        if total == 0:
            return None
        
        positive_pct = (sentiment_counts.get('POSITIVE', 0) / total) * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="number+gauge+delta",
            value=positive_pct,
            title={'text': "Positive Sentiment %"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green" if positive_pct >= 50 else "orange" if positive_pct >= 33 else "red"},
                'steps': [
                    {'range': [0, 33], 'color': "lightcoral"},
                    {'range': [33, 66], 'color': "lightyellow"},
                    {'range': [66, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        return fig
    
    def create_sentiment_trend(self, df: pd.DataFrame) -> Optional[go.Figure]:
        """Create sentiment trend over time"""
        if df.empty or len(df) < 2:
            return None
        
        df_copy = df.copy()
        df_copy['time_bucket'] = df_copy['timestamp'].dt.floor('1min')
        
        trend_data = df_copy.groupby(['time_bucket', 'sentiment']).size().unstack(fill_value=0)
        
        if trend_data.empty:
            return None
        
        trend_data_pct = trend_data.div(trend_data.sum(axis=1), axis=0) * 100
        
        fig = go.Figure()
        
        for sentiment in ['POSITIVE', 'NEUTRAL', 'NEGATIVE']:
            if sentiment in trend_data_pct.columns:
                color = {'POSITIVE': '#00cc66', 'NEUTRAL': '#ffcc00', 'NEGATIVE': '#ff3333'}.get(sentiment, '#808080')
                fig.add_trace(go.Scatter(
                    x=trend_data_pct.index,
                    y=trend_data_pct[sentiment],
                    name=sentiment,
                    mode='lines+markers',
                    line=dict(width=3, color=color),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title='Sentiment Trend Over Time',
            xaxis_title='Time',
            yaxis_title='Percentage (%)',
            hovermode='x unified',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            height=350
        )
        
        return fig
    
    def create_sentiment_distribution(self, df: pd.DataFrame) -> Optional[go.Figure]:
        """Create sentiment distribution pie chart"""
        if df.empty:
            return None
        
        sentiment_counts = df['sentiment'].value_counts()
        
        colors = {'POSITIVE': '#00cc66', 'NEUTRAL': '#ffcc00', 'NEGATIVE': '#ff3333'}
        color_map = [colors.get(sent, '#808080') for sent in sentiment_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            hole=.4,
            marker=dict(colors=color_map),
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Sentiment Distribution',
            showlegend=False,
            height=350
        )
        
        return fig
    
    def create_wordcloud(self, df: pd.DataFrame) -> Optional[plt.Figure]:
        """Create word cloud from text data"""
        if df.empty:
            return None
        
        all_text = ' '.join(df['text'].values)
        all_text = re.sub(r'[^\w\s]', '', all_text.lower())
        
        try:
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='viridis',
                max_words=100,
                contour_width=3,
                contour_color='steelblue'
            ).generate(all_text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            plt.tight_layout()
            return fig
        except Exception as e:
            st.warning(f"Could not generate word cloud: {e}")
            return None
    
    def create_platform_sentiment(self, df: pd.DataFrame) -> Optional[go.Figure]:
        """Create sentiment distribution by platform"""
        if df.empty or 'platform' not in df.columns:
            return None
        
        platform_sentiment = df.groupby(['platform', 'sentiment']).size().unstack(fill_value=0)
        
        if platform_sentiment.empty:
            return None
        
        fig = go.Figure()
        
        colors = {'POSITIVE': '#00cc66', 'NEUTRAL': '#ffcc00', 'NEGATIVE': '#ff3333'}
        
        for sentiment in ['POSITIVE', 'NEUTRAL', 'NEGATIVE']:
            if sentiment in platform_sentiment.columns:
                fig.add_trace(go.Bar(
                    name=sentiment,
                    x=platform_sentiment.index,
                    y=platform_sentiment[sentiment],
                    text=platform_sentiment[sentiment],
                    textposition='auto',
                    marker_color=colors.get(sentiment, '#808080')
                ))
        
        fig.update_layout(
            title='Sentiment by Platform',
            barmode='stack',
            xaxis_title='Platform',
            yaxis_title='Count',
            hovermode='x',
            height=350
        )
        
        return fig

def main():
    """Main dashboard function"""
    st.title("📊 Real-Time Social Media Sentiment Dashboard")
    st.markdown("---")
    
    # Initialize dashboard
    dashboard = SentimentDashboard()
    
    # Sidebar filters
    st.sidebar.header("🎛️ Filters")
    
    time_range = st.sidebar.selectbox(
        "Time Range",
        ["Last 5 minutes", "Last 15 minutes", "Last 30 minutes", "Last hour", "Last 3 hours", "Last 6 hours", "Last 12 hours", "Last 24 hours"],
        index=1
    )
    
    sentiment_filter = st.sidebar.multiselect(
        "Sentiment Filter",
        ["POSITIVE", "NEUTRAL", "NEGATIVE"],
        default=["POSITIVE", "NEUTRAL", "NEGATIVE"]
    )
    
    platform_filter = st.sidebar.multiselect(
        "Platform Filter",
        ["twitter", "reddit", "facebook"],
        default=["twitter", "reddit", "facebook"]
    )
    
    # Auto-refresh
    st.sidebar.markdown("---")
    st.sidebar.header("🔄 Auto Refresh")
    auto_refresh = st.sidebar.checkbox("Enable Auto Refresh", value=True)
    refresh_interval = st.sidebar.slider(
        "Refresh Interval (seconds)",
        min_value=2,
        max_value=30,
        value=5
    )
    
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Time range mapping
    time_mapping = {
        "Last 5 minutes": 5,
        "Last 15 minutes": 15,
        "Last 30 minutes": 30,
        "Last hour": 60,
        "Last 3 hours": 180,
        "Last 6 hours": 360,
        "Last 12 hours": 720,
        "Last 24 hours": 1440
    }
    
    # Fetch data
    df = dashboard.get_latest_data(limit=1000)
    
    # Filter data
    if not df.empty:
        minutes = time_mapping.get(time_range, 60)
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        df = df[df['timestamp'] >= cutoff]
        
        if sentiment_filter:
            df = df[df['sentiment'].isin(sentiment_filter)]
        
        if platform_filter and 'platform' in df.columns:
            df = df[df['platform'].isin(platform_filter)]
        
        df = df.sort_values('timestamp', ascending=True)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📝 Total Posts",
            len(df) if not df.empty else 0
        )
    
    with col2:
        if not df.empty:
            positive_pct = (df['sentiment'] == 'POSITIVE').sum() / len(df) * 100
            st.metric(
                "😊 Positive %",
                f"{positive_pct:.1f}%",
                delta=f"{positive_pct - 50:.1f}%" if positive_pct != 50 else None
            )
        else:
            st.metric("😊 Positive %", "0%")
    
    with col3:
        if not df.empty:
            negative_pct = (df['sentiment'] == 'NEGATIVE').sum() / len(df) * 100
            st.metric(
                "😞 Negative %",
                f"{negative_pct:.1f}%",
                delta=f"{negative_pct - 25:.1f}%" if negative_pct != 25 else None
            )
        else:
            st.metric("😞 Negative %", "0%")
    
    with col4:
        if not df.empty:
            neutral_pct = (df['sentiment'] == 'NEUTRAL').sum() / len(df) * 100
            st.metric(
                "😐 Neutral %",
                f"{neutral_pct:.1f}%",
                delta=f"{neutral_pct - 25:.1f}%" if neutral_pct != 25 else None
            )
        else:
            st.metric("😐 Neutral %", "0%")
    
    st.markdown("---")
    
    if df.empty:
        st.info("📊 No data available. Waiting for first data points...")
        st.info("💡 Make sure the producer and processor services are running.")
    else:
        # Main charts layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Sentiment Trend
            trend_fig = dashboard.create_sentiment_trend(df)
            if trend_fig:
                st.plotly_chart(trend_fig, use_container_width=True)
            else:
                st.info("Not enough data points for trend analysis")
        
        with col2:
            # Sentiment Distribution
            dist_fig = dashboard.create_sentiment_distribution(df)
            if dist_fig:
                st.plotly_chart(dist_fig, use_container_width=True)
        
        # Second row
        col1, col2 = st.columns(2)
        
        with col1:
            # Platform Sentiment
            platform_fig = dashboard.create_platform_sentiment(df)
            if platform_fig:
                st.plotly_chart(platform_fig, use_container_width=True)
            else:
                st.info("No platform data available")
        
        with col2:
            # Word Cloud
            wordcloud_fig = dashboard.create_wordcloud(df)
            if wordcloud_fig:
                st.pyplot(wordcloud_fig)
            else:
                st.info("Not enough text data for word cloud")
        
        # Recent posts
        st.markdown("---")
        st.subheader("📋 Recent Posts")
        
        recent_df = df.nlargest(10, 'timestamp')
        for _, row in recent_df.iterrows():
            sentiment = row['sentiment']
            color = {
                'POSITIVE': '#00cc66',
                'NEUTRAL': '#ffcc00',
                'NEGATIVE': '#ff3333'
            }.get(sentiment, '#808080')
            
            confidence = row.get('sentiment_confidence', 0)
            
            st.markdown(f"""
            <div style="border-left: 5px solid {color}; padding: 10px; margin: 5px 0; background-color: #f8f9fa; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 16px; color: #333;">{row['text']}</span>
                    <span style="font-weight: bold; color: {color};">{sentiment}</span>
                </div>
                <div style="font-size: 12px; color: #666;">
                    Confidence: {confidence:.2%} | 
                    Platform: {row.get('platform', 'unknown')} | 
                    {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-refresh logic
    if auto_refresh and not df.empty:
        import time as time_module
        time_module.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()