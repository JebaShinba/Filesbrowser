import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_mongodb():
    """
    Set up the MongoDB connection and insert test data.
    """
    # Retrieve MongoDB URI from environment variable
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Ping to check connection
        logger.info("MongoDB connected successfully!")
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        exit(1)

    # Set up test data (example)
    db = client.get_database('sampleupload')  # Use a database for testing
    collection = db.get_collection('users')  # Use your actual collection name

    # Example: Insert some test documents
    sample_data = [
        {
            "_id": ObjectId("671f70b2f11c1401cbf07edd"),
            "username": "",
            "first_name": "admin",
            "last_name": "admin",
            "password": "demo",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {"info": "this 'notes' field exists only for this default admin user", "p": "donttrustyou"},
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "success",
            "createdAt": datetime(2024, 10, 28, 11, 8, 34)
        },
        {
            "_id": ObjectId("671f71988a76e1c09ab851f2"),
            "username": "",
            "first_name": "admin",
            "last_name": "admin",
            "password": "demo",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {"info": "this 'notes' field exists only for this default admin user", "p": "donttrustyou"},
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": datetime(2024, 10, 28, 11, 12, 24)
        },
        {
            "_id": ObjectId("671f71abd6fb19d91c706fb4"),
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {"info": "this 'notes' field exists only for this default admin user", "p": "donttrustyou"},
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": datetime(2024, 10, 28, 11, 12, 43)
        },
        {
            "_id": ObjectId("671f44297ff62ef35ec47a47"),
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "demo",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,  # Corrected null to None
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": True,
            "expected_error": "success",
            "createdAt": datetime(2024, 10, 28, 7, 58, 33, 761000)
        }
    ]
    
    # Insert test documents into MongoDB collection
    try:
        collection.insert_many(sample_data)
        logger.info(f"Test data inserted into {db.name}.{collection.name}")
    except Exception as e:
        logger.error(f"Failed to insert test data: {e}")
        exit(1)

if __name__ == "__main__":
    setup_mongodb()
