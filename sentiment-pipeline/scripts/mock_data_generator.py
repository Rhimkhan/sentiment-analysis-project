"""
Generates mock tweet data for Kafka producer testing.
"""

import json
import os
import random
import time
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sentiment_tweets')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

MOCK_TWEETS = [
    'I love this product!',
    'This is the worst thing I have ever bought.',
    'The experience was okay, not great.',
    'Amazing service and fast delivery.',
    'The product quality was disappointing.',
    'I would definitely buy this again.',
    'Terrible, do not recommend.',
    'Just average. Nothing special.',
    'Super impressed with the results!',
    'The price is too high for what you get.'
]

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def generate_tweet() -> dict:
    text = random.choice(MOCK_TWEETS)
    return {
        'id': f'mock_{int(time.time() * 1000)}_{random.randint(1000,9999)}',
        'text': text,
        'created_at': datetime.utcnow().isoformat(),
        'author_id': f'user_{random.randint(1000,9999)}',
        'username': f'user_{random.randint(1000,9999)}',
        'name': f'User {random.randint(1,999)}',
        'retweet_count': random.randint(0, 50),
        'like_count': random.randint(0, 200),
        'source': 'mock'
    }


def run(num_messages: int = 50, delay_seconds: float = 0.5) -> None:
    for _ in range(num_messages):
        tweet = generate_tweet()
        producer.send(KAFKA_TOPIC, key=tweet['id'].encode('utf-8'), value=tweet)
        print(f"Sent: {tweet['id']} -> {tweet['text']}")
        time.sleep(delay_seconds)
    producer.flush()


if __name__ == '__main__':
    run()
