import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
MONGO_URI = "mongodb://127.0.0.1:27017/"  # MongoDB URI
DATABASE_NAME = "sampleupload"  # Your database name
USER_COLLECTION = "users"  # Your collection name
def setup_mongodb():
    # Retrieve MongoDB URI from environment variable if set
    mongo_uri = os.getenv("MONGO_URI", MONGO_URI)
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Ping to check connection
        print("MongoDB connected successfully!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        exit(1)
    # Set up test data (example)
    db = client.get_database(DATABASE_NAME)  # Use your actual database
    collection = db.get_collection(USER_COLLECTION)  # Use your collection
  # Example: Insert some test documents
    sample_data = [
        {
            "username": "testuser1",
            "password": "password123",
            "email": "user1@test.com",
            "is_valid": True,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/"
        },
        {
            "username": "testuser2",
            "password": "password456",
            "email": "user2@test.com",
            "is_valid": True,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/"
        }
    ]
    collection.insert_many(sample_data)
    print(f"Test data inserted into {db.name}.{collection.name}")
if __name__ == "__main__":
    setup_mongodb()