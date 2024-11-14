import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId  # Import ObjectId for MongoDB

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
            "_id": ObjectId("67330291d2ea7592d81572ae"),
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "demo",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-11-05T06:14:52.021Z"
        },
        {
            "_id": ObjectId("6729bf3c523f6133a28fc714"),
            "username": "Test",
            "first_name": "Test",
            "last_name": "one",
            "password": "test",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "iloveyou"
            },
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-11-05T05:55:09.495Z"
        }
    ]
    collection.insert_many(sample_data)
    print(f"Test data inserted into {db.name}.{collection.name}")

if __name__ == "__main__":
    setup_mongodb()
