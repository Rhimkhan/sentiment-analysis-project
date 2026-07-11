# SentimentIQ Architecture

## Overview
SentimentIQ is designed as a modular real-time pipeline with clear separation of concerns:

- `src/producer/` — collects tweets from Twitter or mock sources and publishes them to Kafka.
- `src/consumer/` — consumes Kafka messages, runs sentiment analysis, and stores results in MongoDB.
- `src/storage/` — provides MongoDB helpers for insert and query operations.
- `src/dashboard/` — renders the processed sentiment data in a Streamlit dashboard.

## Data Flow
1. Producer fetches or generates tweets.
2. Producer publishes tweets to Kafka topic `sentiment_tweets`.
3. Consumer reads tweets from Kafka and applies sentiment models.
4. Processed tweets are stored in MongoDB.
5. Dashboard reads processed data from MongoDB and visualizes results.

## Components
### Producer
- `src.producer.twitter_producer.TwitterKafkaProducer`
- `src.producer.twitter_producer.TwitterAPIClient`
- `src.producer.twitter_producer.MockDataGenerator`

### Consumer
- `src.consumer.sentiment_consumer.SentimentConsumer`
- `src.consumer.model_loader.SentimentModelFactory`

### Storage
- `src.storage.mongodb_handler.MongoDBHandler`

### Dashboard
- `src.dashboard.app`

## Startup Goals
- Real-time ingestion and processing
- Docker Compose-based local stack
- Clear developer onboarding with VS Code configs
- Production-organized code and documentation
