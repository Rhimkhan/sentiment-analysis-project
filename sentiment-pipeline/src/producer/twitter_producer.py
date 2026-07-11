"""
Real-time Data Producer using Twitter API v2 or mock data.
Publishes tweets to Kafka topic `sentiment_tweets`.
"""

import json
import os
import random
import time
import logging
from datetime import datetime
from typing import Dict, List

import requests
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

# Load configuration from environment
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sentiment_tweets')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
SEARCH_TERMS = os.getenv('SEARCH_TERMS', 'Tesla,Bitcoin,ChatGPT,Narendra Modi,Cricket').split(',')
MAX_RESULTS = int(os.getenv('TWITTER_MAX_RESULTS', '10'))
PRODUCE_INTERVAL = int(os.getenv('PRODUCE_INTERVAL', '5'))
USE_MOCK = os.getenv('USE_MOCK', 'true').lower() == 'true'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

MOCK_TWEETS = [
    "This is absolutely amazing! Best product ever! 🚀",
    "Complete waste of money. Very disappointed.",
    "The service was okay, nothing special.",
    "I love this! Can't wait for the next update!",
    "Bad customer support. They never respond.",
    "Good product but overpriced.",
    "This changed my life forever! Thank you so much!",
    "Horrible experience. Would not recommend.",
    "Decent quality. Works as expected.",
    "Incredible! Mind-blowing technology! 🤯",
    "The worst purchase I ever made.",
    "Pretty good, but could be better.",
    "Absolutely fantastic! 5 stars! ⭐⭐⭐⭐⭐",
    "Not worth it. Buy something else.",
    "Life-changing product! I'm a fan forever!"
]


class TwitterKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=3,
            compression_type='gzip',
            request_timeout_ms=20000,
            max_block_ms=60000
        )
        logger.info(f"Kafka producer connected to {KAFKA_BOOTSTRAP_SERVERS}")

    def publish_tweet(self, tweet: Dict) -> bool:
        try:
            future = self.producer.send(
                KAFKA_TOPIC,
                key=tweet.get('id', str(time.time())).encode('utf-8'),
                value=tweet
            )
            metadata = future.get(timeout=10)
            logger.debug(f"Published tweet {tweet.get('id')} partition={metadata.partition} offset={metadata.offset}")
            return True
        except Exception as exc:
            logger.error(f"Failed to publish tweet: {exc}")
            return False

    def close(self):
        self.producer.flush()
        self.producer.close()
        logger.info("Kafka producer closed")


class TwitterAPIClient:
    def __init__(self):
        self.bearer_token = TWITTER_BEARER_TOKEN
        self.base_url = 'https://api.twitter.com/2/tweets/search/recent'
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.bearer_token}'})

    def fetch_recent_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        params = {
            'query': f'{query} lang:en -is:retweet',
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,author_id,public_metrics',
            'expansions': 'author_id',
            'user.fields': 'username,name'
        }
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            payload = response.json()
            tweets = []
            users = {user['id']: user for user in payload.get('includes', {}).get('users', [])}
            for raw in payload.get('data', []):
                author = users.get(raw.get('author_id'), {})
                tweets.append({
                    'id': raw.get('id'),
                    'text': raw.get('text', ''),
                    'created_at': raw.get('created_at', datetime.utcnow().isoformat()),
                    'author_id': raw.get('author_id'),
                    'username': author.get('username', ''),
                    'name': author.get('name', ''),
                    'retweet_count': raw.get('public_metrics', {}).get('retweet_count', 0),
                    'like_count': raw.get('public_metrics', {}).get('like_count', 0),
                    'query': query,
                    'source': 'twitter'
                })
            return tweets
        except Exception as exc:
            logger.error(f"Twitter API fetch failed: {exc}")
            return []

    def close(self):
        self.session.close()


class MockDataGenerator:
    @staticmethod
    def generate_mock_tweet() -> Dict:
        text = random.choice(MOCK_TWEETS)
        return {
            'id': f"mock_{int(time.time() * 1000)}_{random.randint(1000,9999)}",
            'text': text,
            'created_at': datetime.utcnow().isoformat(),
            'author_id': f'user_{random.randint(1000,9999)}',
            'username': f'user_{random.randint(1000,9999)}',
            'name': f'User {random.randint(1,100)}',
            'retweet_count': random.randint(0, 50),
            'like_count': random.randint(0, 100),
            'source': 'mock'
        }


def run_producer(use_mock: bool = USE_MOCK, interval_seconds: int = PRODUCE_INTERVAL):
    producer = TwitterKafkaProducer()
    data_source = MockDataGenerator() if use_mock or not TWITTER_BEARER_TOKEN else TwitterAPIClient()

    try:
        while True:
            tweets = []
            if isinstance(data_source, TwitterAPIClient):
                for term in SEARCH_TERMS:
                    tweets.extend(data_source.fetch_recent_tweets(term, max_results=MAX_RESULTS))
                    time.sleep(1)
            else:
                tweets = [MockDataGenerator.generate_mock_tweet() for _ in range(5)]

            for tweet in tweets:
                tweet['ingested_at'] = datetime.utcnow().isoformat()
                success = producer.publish_tweet(tweet)
                if success:
                    logger.info(f"Published tweet id={tweet['id']} text={tweet['text'][:60]}")
                else:
                    logger.warning(f"Publish failed for id={tweet['id']}")

            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logger.info('Producer interrupted')
    finally:
        producer.close()
        if isinstance(data_source, TwitterAPIClient):
            data_source.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Twitter Kafka Producer')
    parser.add_argument('--mock', action='store_true', help='Use mock data instead of Twitter API')
    parser.add_argument('--interval', type=int, default=PRODUCE_INTERVAL, help='Interval between batches')
    args = parser.parse_args()

    run_producer(use_mock=args.mock, interval_seconds=args.interval)
