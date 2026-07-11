import os
from dotenv import load_dotenv

load_dotenv()

class ProducerConfig:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'social_sentiment')
    PRODUCE_INTERVAL = int(os.getenv('PRODUCE_INTERVAL', 2))
    
    # Sample data sources
    SAMPLE_TEXTS = [
        "I absolutely love this product! It's amazing!",
        "This is the worst service I've ever experienced.",
        "The movie was okay, nothing special.",
        "What a wonderful day to be alive!",
        "I'm feeling quite neutral about this situation.",
        "The customer support was incredibly helpful and responsive.",
        "My package arrived damaged. Very disappointed.",
        "Just had the best meal of my life!",
        "This software is buggy and crashes constantly.",
        "Not sure how I feel about this new policy.",
        "The team did an excellent job on this project!",
        "I hate waiting in long lines.",
        "The presentation was informative but a bit boring.",
        "What an amazing performance by the cast!",
        "The product is decent for the price.",
        "Terrible experience, would not recommend.",
        "I'm so excited about the upcoming event!",
        "The quality has really declined over the years.",
        "This is exactly what I was looking for!",
        "I have mixed feelings about the new design."
    ]

producer_config = ProducerConfig()