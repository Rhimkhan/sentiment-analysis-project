"""
Sentiment Analysis Model Loader
Supports VADER, TextBlob, DistilBERT, RoBERTa, and ensemble inference.
"""

import logging
import re
from typing import Dict, Tuple, List, Optional

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BaseSentimentModel:
    def analyze(self, text: str) -> Dict[str, float]:
        raise NotImplementedError

    def get_sentiment_label(self, text: str) -> Tuple[str, float]:
        raise NotImplementedError


class VADERSentiment(BaseSentimentModel):
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        logger.info('Loaded VADER sentiment model')

    def analyze(self, text: str) -> Dict[str, float]:
        scores = self.analyzer.polarity_scores(text)
        return {
            'positive': float(scores['pos']),
            'negative': float(scores['neg']),
            'neutral': float(scores['neu']),
            'compound': float(scores['compound'])
        }

    def get_sentiment_label(self, text: str) -> Tuple[str, float]:
        scores = self.analyze(text)
        compound = scores['compound']
        if compound >= 0.05:
            return 'positive', compound
        if compound <= -0.05:
            return 'negative', abs(compound)
        return 'neutral', abs(compound)


class TextBlobSentiment(BaseSentimentModel):
    def analyze(self, text: str) -> Dict[str, float]:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return {'positive': float(polarity), 'negative': 0.0, 'neutral': float(1 - polarity)}
        if polarity < 0:
            return {'positive': 0.0, 'negative': float(-polarity), 'neutral': float(1 + polarity)}
        return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}

    def get_sentiment_label(self, text: str) -> Tuple[str, float]:
        scores = self.analyze(text)
        label = max(['positive', 'negative', 'neutral'], key=lambda k: scores[k])
        return label, float(scores[label])


class TransformerSentiment(BaseSentimentModel):
    MODEL_MAP = {
        'distilbert': 'distilbert-base-uncased-finetuned-sst-2-english',
        'roberta': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
        'bert': 'nlptown/bert-base-multilingual-uncased-sentiment'
    }

    def __init__(self, model_name: str = 'distilbert', device: str = 'cpu'):
        self.model_name = self.MODEL_MAP.get(model_name, model_name)
        self.device = 0 if device == 'gpu' and torch.cuda.is_available() else -1
        self.pipeline = pipeline('sentiment-analysis', model=self.model_name, tokenizer=self.model_name, device=self.device)
        self.labels = ['negative', 'neutral', 'positive'] if 'roberta' in self.model_name else ['negative', 'positive']
        logger.info(f'Loaded Transformer model {self.model_name} on device {self.device}')

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return re.sub(r'\s+', ' ', text).strip()

    def analyze(self, text: str) -> Dict[str, float]:
        cleaned = self._clean_text(text[:512])
        result = self.pipeline(cleaned)[0]
        label = result['label']
        score = float(result['score'])
        if 'roberta' in self.model_name and label.startswith('LABEL_'):
            label_idx = int(label.split('_')[-1])
            label = self.labels[label_idx]
        if label.upper() == 'POSITIVE':
            return {'positive': score, 'negative': 0.0, 'neutral': 1.0 - score}
        return {'positive': 0.0, 'negative': score, 'neutral': 1.0 - score}

    def get_sentiment_label(self, text: str) -> Tuple[str, float]:
        scores = self.analyze(text)
        label = max(['positive', 'negative', 'neutral'], key=lambda k: scores.get(k, 0.0))
        return label, float(scores.get(label, 0.0))


class EnsembleSentiment(BaseSentimentModel):
    def __init__(self, models: Optional[List[str]] = None, device: str = 'cpu'):
        self.models = models or ['vader', 'distilbert']
        self.device = device
        self.model_instances = []
        for model_name in self.models:
            if model_name == 'vader':
                self.model_instances.append(VADERSentiment())
            elif model_name == 'textblob':
                self.model_instances.append(TextBlobSentiment())
            else:
                self.model_instances.append(TransformerSentiment(model_name, device))
        logger.info(f'Loaded ensemble models: {self.models}')

    def analyze(self, text: str) -> Dict[str, float]:
        combined = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
        weights = [0.3] * len(self.model_instances)
        for model, weight in zip(self.model_instances, weights):
            scores = model.analyze(text)
            for label in combined:
                combined[label] += float(scores.get(label, 0.0)) * weight
        total = sum(combined.values())
        if total > 0:
            for label in combined:
                combined[label] /= total
        return combined

    def get_sentiment_label(self, text: str) -> Tuple[str, float]:
        scores = self.analyze(text)
        label = max(scores, key=scores.get)
        return label, float(scores[label])


class SentimentModelFactory:
    @staticmethod
    def get_model(model_name: str = 'vader', device: str = 'cpu') -> BaseSentimentModel:
        if model_name == 'vader':
            return VADERSentiment()
        elif model_name == 'textblob':
            return TextBlobSentiment()
        elif model_name in ['distilbert', 'roberta', 'bert']:
            return TransformerSentiment(model_name, device)
        elif model_name == 'ensemble':
            return EnsembleSentiment(['vader', 'distilbert'], device)
        else:
            raise ValueError(f'Unknown model {model_name}')
