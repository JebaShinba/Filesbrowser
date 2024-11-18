from pymongo import MongoClient

MONGO_URI = "mongodb://127.0.0.1:27017/"
DATABASE_NAME = "your_database_name"  # Use your actual database name
USER_COLLECTION = "users"  # Corrected variable name
FILES_COLLECTION = "files"

def get_db():
    """Connect to MongoDB and return the database instance."""
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db

def get_users_collection():
    """Get the users collection from the database."""
    db = get_db()
    user_collection = db[USER_COLLECTION]  # Corrected to use a single bracket

    return user_collection  # Return the users collection

def get_files_collection():
    """Get the users collection from the database."""
    db = get_db()
    files_collection = db[FILES_COLLECTION]  # Corrected to use a single bracket

    return files_collection  # Return the users collection