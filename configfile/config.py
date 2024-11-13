import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from bson import ObjectId  # Import ObjectId to handle _id fields

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

    # Set up test data
    db = client.get_database(DATABASE_NAME)  # Use your actual database
    collection = db.get_collection(USER_COLLECTION)  # Use your collection

    # Sample data to insert into MongoDB (user details)
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
        },
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
        },
        {
            "_id": "671f70b2f11c1401cbf07edd",
            "username": "",
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
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "success",
            "createdAt": "2024-10-28T11:08:34.507Z"
        },
        {
            "_id": "671f71988a76e1c09ab851f2",
            "username": "",
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
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-10-28T11:12:24.055Z"
        },
        {
            "_id": "671f71abd6fb19d91c706fb4",
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-10-28T11:12:43.404Z"
        },
        {
            "_id": "671f71b54b69104645e37af0",
            "username": "",
            "first_name": "admin",
            "last_name": "admin",
            "password": "",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-10-28T11:12:53.301Z"
        },
        {
            "_id": "671f71d442086dc454e456e2",
            "username": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
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
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-10-28T11:13:24.743Z"
        },
        {
            "_id": "671f71eeeedc4f47ad6bd681",
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "dqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-10-28T11:13:50.894Z"
        },
        {
            "_id": "671f726f4b0562c323398397",
            "username": "demo",
            "first_name": "admin",
            "last_name": "admin",
            "password": "          ",
            "mode_2fa": "Off",
            "groups": ["Admin"],
            "rights": "Admin",
            "notes": {
                "info": "this 'notes' field exists only for this default admin user",
                "p": "donttrustyou"
            },
            "vec_2fa": None,
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/",
            "is_valid": False,
            "expected_error": "Wrong credentials",
            "createdAt": "2024-10-28T11:15:59.889Z"
        },
    ]

    # Insert or update data
    for data in sample_data:
        try:
            collection.update_one(
                {"_id": data.get("_id")},  # Check by _id
                {"$set": data},  # Update the document with new data
                upsert=True  # Insert if not found
            )
            print(f"Inserted/Updated: {data.get('username')}")
        except DuplicateKeyError as e:
            print(f"Duplicate key error for user: {data.get('username')}. Skipping.")
        except Exception as e:
            print(f"Error inserting/updating user {data.get('username')}: {e}")

if __name__ == "__main__":
    setup_mongodb()
