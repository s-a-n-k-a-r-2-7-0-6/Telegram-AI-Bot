import os
import pymongo
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["telegram_bot"]
users_collection = db["users"]
chat_collection = db["chats"]
files_collection = db["files"]

# Function to add a new user
def add_user(chat_id, first_name, username, phone_number=None):
    user = {"chat_id": chat_id, "first_name": first_name, "username": username, "phone": phone_number}
    users_collection.update_one({"chat_id": chat_id}, {"$set": user}, upsert=True)

# Function to store chat messages with timestamp
def save_chat(chat_id, user_message, bot_response):
    timestamp = datetime.now()  # Capture current timestamp
    chat_collection.insert_one({
        "chat_id": chat_id, 
        "user": user_message, 
        "bot": bot_response, 
        "timestamp": timestamp  # Add timestamp to the stored document
    })
