"""
Stream Processor module for Real-Time Sentiment Analysis
Handles Kafka consumption and sentiment analysis
"""

from .consumer import SentimentProcessor
from .sentiment_analyzer import SentimentAnalyzer
from .config import processor_config

__all__ = ['SentimentProcessor', 'SentimentAnalyzer', 'processor_config']