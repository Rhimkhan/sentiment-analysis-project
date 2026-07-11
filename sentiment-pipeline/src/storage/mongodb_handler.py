"""
MongoDB Storage Handler for sentiment pipeline.
"""

import logging
from pymongo import MongoClient
from pymongo.collection import Collection

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MongoDBHandler:
    def __init__(self, uri: str, database: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.collection: Collection = self.db[collection_name]
        self.collection.create_index('id', unique=True)
        self.collection.create_index('sentiment.label')
        self.collection.create_index('processed_at')
        logger.info(f'MongoDB connected to {uri}, db={database}, collection={collection_name}')

    def insert_processed_tweet(self, tweet: dict) -> bool:
        try:
            self.collection.update_one(
                {'id': tweet.get('id')},
                {'$set': tweet},
                upsert=True
            )
            return True
        except Exception as exc:
            logger.error(f'Error inserting tweet into MongoDB: {exc}')
            return False

    def get_recent_tweets(self, limit: int = 100) -> list[dict]:
        return list(self.collection.find({}, sort=[('processed_at', -1)], limit=limit))

    def get_sentiment_summary(self) -> dict:
        pipeline = [
            {'$group': {'_id': '$sentiment.label', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ]
        return {entry['_id']: entry['count'] for entry in self.collection.aggregate(pipeline)}

    def close(self):
        self.client.close()
        logger.info('MongoDB connection closed')
