"""
Streamlit dashboard for sentiment analysis results.
"""

import os
import logging
from typing import Any
import streamlit as st
from src.storage.mongodb_handler import MongoDBHandler
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'sentiment_db')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'processed_tweets')
APP_TITLE = os.getenv('APP_TITLE', 'Sentiment Analysis Dashboard')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_data(handler: MongoDBHandler, limit: int = 100) -> dict[str, Any]:
    recent = handler.get_recent_tweets(limit)
    summary = handler.get_sentiment_summary()
    return {'recent_tweets': recent, 'summary': summary}


def render_dashboard(data: dict[str, Any]) -> None:
    st.title(APP_TITLE)
    st.markdown('### Real-time sentiment stream')

    summary = data['summary']
    st.subheader('Sentiment Distribution')
    st.write(summary)

    st.subheader('Recent Processed Tweets')
    st.dataframe(data['recent_tweets'])

    if data['recent_tweets']:
        positive = summary.get('positive', 0)
        negative = summary.get('negative', 0)
        neutral = summary.get('neutral', 0)
        total = positive + negative + neutral
        if total > 0:
            st.metric('Positive', positive)
            st.metric('Negative', negative)
            st.metric('Neutral', neutral)
            st.metric('Total Processed', total)

            chart_data = {
                'label': ['positive', 'negative', 'neutral'],
                'count': [positive, negative, neutral]
            }
            st.bar_chart(chart_data)


def main() -> None:
    handler = MongoDBHandler(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
    data = load_data(handler, limit=100)
    render_dashboard(data)
    handler.close()


if __name__ == '__main__':
    main()
