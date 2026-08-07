"""Small MongoDB repository used by authentication and AI chat APIs."""
import os
from functools import lru_cache
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError


@lru_cache(maxsize=1)
def get_database():
    uri = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI') or os.getenv('MongoURI')
    if not uri:
        raise RuntimeError('MONGODB_URI is not configured in Backend/.env')
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    database = client.get_default_database(default=os.getenv('MONGODB_DB_NAME', 'kbtech'))
    database.users.create_index([('email', ASCENDING)], unique=True)
    database.sessions.create_index([('token', ASCENDING)], unique=True)
    database.sessions.create_index([('expires_at', ASCENDING)], expireAfterSeconds=0)
    database.chat_messages.create_index([('user_id', ASCENDING), ('created_at', DESCENDING)])
    database.seasonal_disease_advice.create_index([('date', ASCENDING), ('season', ASCENDING)], unique=True)
    return database


def mongo_error_message(error: Exception) -> str:
    return 'MongoDB is unavailable. Check MONGODB_URI and network access.' if isinstance(error, PyMongoError) else str(error)
