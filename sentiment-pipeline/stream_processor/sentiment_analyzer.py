import logging
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Handles sentiment analysis using pre-trained transformer models"""
    
    def __init__(self, model_name: str, max_length: int = 512):
        self.model_name = model_name
        self.max_length = max_length
        self.tokenizer = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.load_model()
    
    def load_model(self):
        """Load tokenizer and model from HuggingFace"""
        try:
            logger.info(f"Loading model {self.model_name} on {self.device}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name
            ).to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text
        Returns: Dict with sentiment label and confidence scores
        """
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding=True
            ).to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                scores = torch.softmax(outputs.logits, dim=1)
                
                # Get predicted class and confidence
                predicted_class = torch.argmax(scores, dim=1).item()
                confidence = scores[0][predicted_class].item()
                
                # Map to sentiment labels
                # RoBERTa model uses: 0=negative, 1=neutral, 2=positive
                sentiment_map = {
                    0: "NEGATIVE",
                    1: "NEUTRAL",
                    2: "POSITIVE"
                }
                
                result = {
                    'sentiment': sentiment_map[predicted_class],
                    'confidence': confidence,
                    'scores': {
                        'negative': scores[0][0].item(),
                        'neutral': scores[0][1].item(),
                        'positive': scores[0][2].item()
                    }
                }
                
                return result
                
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'sentiment': 'ERROR',
                'confidence': 0.0,
                'scores': {'negative': 0.0, 'neutral': 0.0, 'positive': 0.0}
            }
    
    def analyze_batch(self, texts: list) -> list:
        """Analyze sentiment for a batch of texts"""
        return [self.analyze_sentiment(text) for text in texts]