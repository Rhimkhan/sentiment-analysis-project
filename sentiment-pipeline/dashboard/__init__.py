"""
Dashboard module for Real-Time Sentiment Analysis
Provides live visualization and monitoring interface
"""

from .app import main, SentimentDashboard
from .config import dashboard_config

__all__ = ['main', 'SentimentDashboard', 'dashboard_config']