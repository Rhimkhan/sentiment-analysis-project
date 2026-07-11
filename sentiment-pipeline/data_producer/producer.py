import json
import random
import time
import logging
from datetime import datetime
from typing import Dict, List
from kafka import KafkaProducer
from kafka.errors import KafkaError

from .config import producer_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SocialMediaProducer:
    """Simulates real-time social media data stream"""
    
    def __init__(self):
        self.config = producer_config
        self.producer = None
        self.setup_producer()
        
    def setup_producer(self):
        """Initialize Kafka producer with retry logic"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.config.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1,
                compression_type='gzip'
            )
            logger.info(f"Kafka producer connected to {self.config.KAFKA_BOOTSTRAP_SERVERS}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise
    
    def generate_data_point(self) -> Dict:
        """Generate a synthetic data point mimicking social media post"""
        text = random.choice(self.config.SAMPLE_TEXTS)
        return {
            'id': f"post_{int(time.time())}_{random.randint(1000, 9999)}",
            'timestamp': datetime.utcnow().isoformat(),
            'text': text,
            'platform': random.choice(['twitter', 'reddit', 'facebook']),
            'user_id': f"user_{random.randint(1000, 9999)}",
            'location': random.choice([
                'New York', 'London', 'Tokyo', 'Paris', 'Sydney',
                'Berlin', 'Moscow', 'Beijing', 'Singapore', 'Dubai'
            ]),
            'followers': random.randint(10, 100000),
            'retweets': random.randint(0, 1000),
            'likes': random.randint(0, 5000)
        }
    
    def send_message(self, data: Dict):
        """Send message to Kafka topic"""
        try:
            future = self.producer.send(
                self.config.KAFKA_TOPIC,
                value=data
            )
            # Wait for acknowledgment
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Message sent to {record_metadata.topic} "
                f"partition {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )
            return True
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def run(self):
        """Main loop for producing data"""
        logger.info(f"Starting producer with interval {self.config.PRODUCE_INTERVAL}s")
        
        try:
            while True:
                data = self.generate_data_point()
                if self.send_message(data):
                    logger.info(f"Produced: {data['text'][:50]}...")
                else:
                    logger.warning("Failed to produce message, will retry")
                
                time.sleep(self.config.PRODUCE_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Shutting down producer...")
        finally:
            self.producer.close()

if __name__ == "__main__":
    producer = SocialMediaProducer()
    producer.run()