import os
from dotenv import load_dotenv

load_dotenv()

class ProcessorConfig:
    # Kafka Config
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'social_sentiment')
    KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'sentiment_processor')
    
    # Model Config
    MODEL_NAME = os.getenv('MODEL_NAME', 'cardiffnlp/twitter-roberta-base-sentiment-latest')
    MAX_SEQUENCE_LENGTH = int(os.getenv('MAX_SEQUENCE_LENGTH', 512))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 32))
    
    # MongoDB Config
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'sentiment_db')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'processed_data')
    
    # Redis Config
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    REDIS_CACHE_EXPIRE = int(os.getenv('REDIS_CACHE_EXPIRE', 3600))

processor_config = ProcessorConfig()