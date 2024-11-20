import os
import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "sampleupload"
COLLECTION_NAME = "users"

@pytest.fixture(scope="module")
def mongo_client():
    """
    Fixture to set up and return a MongoDB client.
    Tears down the database after tests.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Ping to check connection
        print("MongoDB connected successfully!")
    except ConnectionFailure as e:
        pytest.fail(f"Failed to connect to MongoDB: {e}")

    # Return the client for use in tests
    yield client

    # Teardown: Drop the test database after tests
    client.drop_database(DATABASE_NAME)
    print(f"Database {DATABASE_NAME} dropped after tests.")

@pytest.fixture(scope="module")
def setup_test_data(mongo_client):
    """
    Fixture to insert test data into the MongoDB collection.
    """
    db = mongo_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Insert sample test data
    sample_data = [
        {
            "username": "testuser1", 
            "password": "password123", 
            "email": "user1@test.com", 
            "is_valid": False, 
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/"
        },
        {
            "username": "testuser2", 
            "password": "password456", 
            "email": "user2@test.com", 
            "is_valid": False, 
            "baseurl": "https://demo.filebrowser.org/login?redirect=/files/"
        }
    ]
    collection.insert_many(sample_data)
    print(f"Test data inserted into {DATABASE_NAME}.{COLLECTION_NAME}")

    return collection

def test_mongo_connection(mongo_client):
    """
    Test that MongoDB connection is successful.
    """
    try:
        mongo_client.admin.command('ping')
        assert True, "MongoDB connection test passed."
    except ConnectionFailure:
        pytest.fail("MongoDB connection test failed.")

def test_data_insertion(setup_test_data):
    """
    Test that data is correctly inserted into the collection.
    """
    collection = setup_test_data
    # Assert the number of documents in the collection
    assert collection.count_documents({}) == 2, "Data insertion test passed."
    # Verify specific document
    user = collection.find_one({"username": "testuser1"})
    assert user["email"] == "user1@test.com", "Email verification test passed."
