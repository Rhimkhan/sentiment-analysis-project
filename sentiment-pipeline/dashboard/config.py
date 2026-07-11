import os
from dotenv import load_dotenv

load_dotenv()

class DashboardConfig:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'sentiment_db')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'processed_data')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    UPDATE_INTERVAL = int(os.getenv('DASHBOARD_UPDATE_INTERVAL', 5))

dashboard_config = DashboardConfig()