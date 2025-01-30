import streamlit as st
import pandas as pd
from database import users_collection, chat_collection

# Fetch data from MongoDB
user_count = users_collection.count_documents({})
chat_count = chat_collection.count_documents({})

# Fetch all chat data (questions asked by the user)
chat_data = list(chat_collection.find({}, {"_id": 0, "user": 1, "chat_id": 1, "timestamp": 1}))

# Create a DataFrame from chat data
df_chats = pd.DataFrame(chat_data)

# Map chat_id to username
def get_username_from_chat_id(chat_id):
    user_data = users_collection.find_one({"chat_id": chat_id}, {"username": 1, "_id": 0})
    return user_data["username"] if user_data else "Unknown User"

# Add a new column 'username' in the DataFrame based on chat_id
df_chats['username'] = df_chats['chat_id'].apply(get_username_from_chat_id)

# Streamlit UI
st.title("📊 Telegram Bot Analytics")

# Display Total Users and Chats
st.metric(label="👥 Total Users", value=user_count)
st.metric(label="💬 Total Chats", value=chat_count)

# Display questions asked by the user
st.subheader("📜 Questions Asked by Users")
if not df_chats.empty:
    st.dataframe(df_chats[["username", "user", "timestamp"]].sort_values(by="timestamp", ascending=False))
else:
    st.write("No questions asked yet.")
