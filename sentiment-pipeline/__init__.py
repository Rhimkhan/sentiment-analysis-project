"""
Real-Time Sentiment Analysis Pipeline
A production-ready end-to-end sentiment analysis system
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .data_producer import SocialMediaProducer
from .stream_processor import SentimentProcessor
from .dashboard import SentimentDashboard

__all__ = ['SocialMediaProducer', 'SentimentProcessor', 'SentimentDashboard']
