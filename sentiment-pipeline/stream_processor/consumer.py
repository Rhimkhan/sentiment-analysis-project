import json
import logging
from datetime import datetime
from typing import Dict, Any
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import pymongo
import redis
from .config import processor_config
from .sentiment_analyzer import SentimentAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SentimentProcessor:
    """Processes incoming data through sentiment analysis pipeline"""
    
    def __init__(self):
        self.config = processor_config
        self.consumer = None
        self.db = None
        self.redis_client = None
        self.analyzer = None
        
        self.setup_kafka()
        self.setup_database()
        self.setup_redis()
        self.setup_analyzer()
    
    def setup_kafka(self):
        """Initialize Kafka consumer"""
        try:
            self.consumer = KafkaConsumer(
                self.config.KAFKA_TOPIC,
                bootstrap_servers=self.config.KAFKA_BOOTSTRAP_SERVERS,
                group_id=self.config.KAFKA_GROUP_ID,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                max_poll_records=100
            )
            logger.info(f"Kafka consumer connected to {self.config.KAFKA_BOOTSTRAP_SERVERS}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise
    
    def setup_database(self):
        """Initialize MongoDB connection"""
        try:
            client = pymongo.MongoClient(self.config.MONGO_URI)
            self.db = client[self.config.MONGO_DATABASE]
            # Create indexes for performance
            self.db[self.config.MONGO_COLLECTION].create_index('timestamp')
            self.db[self.config.MONGO_COLLECTION].create_index('sentiment')
            logger.info("MongoDB connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def setup_redis(self):
        """Initialize Redis connection for caching"""
        try:
            self.redis_client = redis.Redis.from_url(
                self.config.REDIS_URL,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def setup_analyzer(self):
        """Initialize sentiment analyzer"""
        self.analyzer = SentimentAnalyzer(
            self.config.MODEL_NAME,
            self.config.MAX_SEQUENCE_LENGTH
        )
    
    def process_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single message through the pipeline"""
        text = data.get('text', '')
        
        # Analyze sentiment
        sentiment_result = self.analyzer.analyze_sentiment(text)
        
        # Enrich data with sentiment
        enriched_data = {
            **data,
            'sentiment': sentiment_result['sentiment'],
            'sentiment_confidence': sentiment_result['confidence'],
            'sentiment_scores': sentiment_result['scores'],
            'processed_timestamp': datetime.utcnow().isoformat()
        }
        
        return enriched_data
    
    def save_to_mongodb(self, data: Dict[str, Any]):
        """Save processed data to MongoDB"""
        try:
            self.db[self.config.MONGO_COLLECTION].insert_one(data)
            logger.debug(f"Data saved to MongoDB: {data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to save to MongoDB: {e}")
    
    def update_redis_cache(self, data: Dict[str, Any]):
        """Update Redis cache with latest aggregated statistics"""
        if not self.redis_client:
            return
        
        try:
            # Update real-time statistics
            key = 'sentiment_stats'
            stats = self.redis_client.get(key)
            if stats:
                stats = json.loads(stats)
            else:
                stats = {
                    'total_processed': 0,
                    'sentiment_counts': {'POSITIVE': 0, 'NEUTRAL': 0, 'NEGATIVE': 0},
                    'total_positive': 0,
                    'total_negative': 0,
                    'total_neutral': 0
                }
            
            stats['total_processed'] += 1
            sentiment = data['sentiment']
            stats['sentiment_counts'][sentiment] = stats['sentiment_counts'].get(sentiment, 0) + 1
            
            # Store with expiration
            self.redis_client.setex(
                key,
                self.config.REDIS_CACHE_EXPIRE,
                json.dumps(stats)
            )
            
            # Cache recent posts
            recent_key = 'recent_posts'
            recent_posts = self.redis_client.lrange(recent_key, 0, 99)
            if len(recent_posts) >= 100:
                self.redis_client.rpop(recent_key)
            self.redis_client.lpush(recent_key, json.dumps(data))
            
        except Exception as e:
            logger.error(f"Failed to update Redis cache: {e}")
    
    def run(self):
        """Main processing loop"""
        logger.info("Starting sentiment processor...")
        
        try:
            for message in self.consumer:
                try:
                    # Process the message
                    enriched_data = self.process_message(message.value)
                    
                    # Store results
                    self.save_to_mongodb(enriched_data)
                    self.update_redis_cache(enriched_data)
                    
                    logger.info(
                        f"Processed: {enriched_data.get('text', '')[:50]}... "
                        f"| Sentiment: {enriched_data['sentiment']} "
                        f"| Confidence: {enriched_data['sentiment_confidence']:.3f}"
                    )
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    continue
                    
        except KeyboardInterrupt:
            logger.info("Shutting down processor...")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    processor = SentimentProcessor()
    processor.run()