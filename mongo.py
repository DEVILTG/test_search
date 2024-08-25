from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, db_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    # Create or get a collection
    def create_collection(self, collection_name):
        return self.db[collection_name]

    # Insert a document into a collection
    def insert_document(self, collection_name, document):
        collection = self.create_collection(collection_name)
        return collection.insert_one(document)

    # Find documents in a collection
    def find_documents(self, collection_name, query=None):
        collection = self.create_collection(collection_name)
        return collection.find(query) if query else collection.find()

    # Update a document in a collection
    def update_document(self, collection_name, query, update_values):
        collection = self.create_collection(collection_name)
        return collection.update_one(query, {"$set": update_values})

    # Delete a document from a collection
    def delete_document(self, collection_name, query):
        collection = self.create_collection(collection_name)
        return collection.delete_one(query)

    # Specific functions for each collection
    def create_users_table(self):
        return self.create_collection("users")

    def create_blocked_users_table(self):
        return self.create_collection("blocked_users")

    def create_anime_links_table(self):
        return self.create_collection("anime_links")

    # Function to add a user
    def add_user(self, user_data):
        return self.insert_document("users", user_data)

    # Function to block a user
    def block_user(self, user_id):
        return self.insert_document("blocked_users", {"user_id": user_id})

    # Function to add an anime link
    def add_anime_link(self, anime_name, anime_link):
        return self.insert_document("anime_links", {"anime_name": anime_name, "anime_link": anime_link})

# Usage example:
if __name__ == "__main__":
    db_handler = MongoDBHandler("your_database_name")

    # Create collections
    db_handler.create_users_table()
    db_handler.create_blocked_users_table()
    db_handler.create_anime_links_table()

    # Add a user
    user_data = {"username": "john_doe", "email": "john@example.com"}
    db_handler.add_user(user_data)

    # Block a user
    db_handler.block_user(user_id=1)

    # Add an anime link
    db_handler.add_anime_link("Naruto", "https://example.com/naruto")
