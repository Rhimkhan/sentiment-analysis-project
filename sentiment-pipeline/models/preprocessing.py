"""
Text preprocessing utilities for sentiment analysis
"""

import re
import string
from typing import List, Optional

class TextPreprocessor:
    """Handles text preprocessing for sentiment analysis"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text for sentiment analysis
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove user mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def tokenize_simple(text: str) -> List[str]:
        """Simple tokenization by splitting on whitespace"""
        return text.split()
    
    @staticmethod
    def remove_stopwords(tokens: List[str], stopwords: Optional[List[str]] = None) -> List[str]:
        """Remove stopwords from token list"""
        if stopwords is None:
            # Basic stopwords list
            stopwords = [
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
                'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
                'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                'until', 'while', 'of', 'at', 'by