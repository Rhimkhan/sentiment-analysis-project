"""
Kafka Consumer - Reads tweets, applies sentiment, stores in MongoDB
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict
from kafka import KafkaConsumer
from pymongo import MongoClient
from src.consumer.model_loader import SentimentModelFactory
from src.storage.mongodb_handler import MongoDBHandler
from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sentiment_tweets')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'sentiment_consumer_group')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'sentiment_db')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'processed_tweets')
SENTIMENT_MODEL = os.getenv('SENTIMENT_MODEL', 'vader')
USE_GPU = os.getenv('USE_GPU', 'false').lower() == 'true'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class SentimentConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=KAFKA_GROUP_ID,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            max_poll_records=100,
            request_timeout_ms=30000,
            session_timeout_ms=30000,
            heartbeat_interval_ms=3000
        )
        self.db = MongoDBHandler(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
        self.model = SentimentModelFactory.get_model(SENTIMENT_MODEL, device='gpu' if USE_GPU else 'cpu')
        self.processed_count = 0
        self.error_count = 0
        logger.info(f"Kafka consumer connected to {KAFKA_BOOTSTRAP_SERVERS} topic={KAFKA_TOPIC}")

    def process_record(self, tweet: Dict) -> Dict:
        text = tweet.get('text', '')
        if not text.strip():
            return None
        label, score = self.model.get_sentiment_label(text)
        return {
            **tweet,
            'sentiment': {
                'label': label,
                'score': float(score)
            },
            'processed_at': datetime.utcnow().isoformat(),
            'text_length': len(text),
            'word_count': len(text.split()),
            'model_used': SENTIMENT_MODEL
        }

    def run(self):
        try:
            for message in self.consumer:
                try:
                    tweet = message.value
                    processed = self.process_record(tweet)
                    if not processed:
                        self.error_count += 1
                        continue
                    self.db.insert_processed_tweet(processed)
                    self.processed_count += 1
                    logger.info(f"Processed tweet id={processed.get('id')} sentiment={processed['sentiment']['label']} score={processed['sentiment']['score']:.2f}")
                except Exception as exc:
                    self.error_count += 1
                    logger.error(f"Error processing message: {exc}")
                    continue
        except KeyboardInterrupt:
            logger.info('Consumer interrupted')
        finally:
            self.close()

    def close(self):
        self.consumer.close()
        self.db.close()
        logger.info(f"Consumer closed. processed={self.processed_count}, errors={self.error_count}")


if __name__ == '__main__':
    consumer = SentimentConsumer()
    consumer.run()
