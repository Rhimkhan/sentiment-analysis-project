"""
Data Producer module for Real-Time Sentiment Analysis
Simulates social media data stream and publishes to Kafka
"""

from .producer import SocialMediaProducer
from .config import producer_config

__all__ = ['SocialMediaProducer', 'producer_config']