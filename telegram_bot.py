import os
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from database import add_user, save_chat
from gemini_chat import get_gemini_response

from telegram import ReplyKeyboardMarkup
from web_search import web_search
from textblob import TextBlob


# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Emojis for responses
emojis = ["😊", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😍", "😎", "🤗", "🤩", "😇",
    "😜", "😝", "😛", "🤔", "🤯", "🤐", "😳", "😏", "😌", "😥", "😢", "😭", "🥺", "😩", "😓",
    "😤", "😠", "😡", "🤬", "😳", "😨", "😰", "😱", "😖", "😞", "😔", "🤢", "🤮", "🥴", "🥳",
    "😷", "🤧", "😵", "😵‍💫", "🤠", "🤑", "😈", "👿", "🤡", "👻", "💀", "☠️", "🤖", "👹", 
    "🎉", "🎁", "🎂", "🎊", "🎈", "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "💖", "💗", 
    "💓", "💕", "💞", "💌", "💘", "💝", "💟",]

# Auto-follow up questions
follow_up_questions = [
    "What else can I assist you with?",
    "Is there anything else you'd like to explore...😁?",
    "Feel free to ask more questions! 😊",
]

# Start command
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    username = update.message.chat.username
    
    add_user(chat_id, first_name, username)
    update.message.reply_text(f"Hello {first_name}! Welcome to the AI Bot. Type your query. 🤖")



# Message handler for Gemini AI chat with emojis and auto-follow-ups
def chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    # Get response from Gemini chat model
    bot_response = get_gemini_response(user_message)
    
    # Add emojis to the bot's response
    emoji_response = f"{bot_response} {random.choice(emojis)}"
    
    # Save the chat to database
    save_chat(chat_id, user_message, bot_response)
    
    # Send bot response with emoji
    update.message.reply_text(emoji_response)

    # Ask an auto-follow-up question
    follow_up = random.choice(follow_up_questions)
    update.message.reply_text(follow_up)

# Set up the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
    dp.add_handler(CommandHandler("websearch", search)) 
    dp.add_handler(CommandHandler("about", about))  # Add this line for 'about' command
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
   
    
    # Start the bot
    updater.start_polling()
    updater.idle()

# Web search command handler
def search(update: Update, context: CallbackContext):
    """Handles /websearch command."""
    if not context.args:
        update.message.reply_text("❌ Please provide a search query. Example: `/websearch AI trends`")
        return
    
    query = " ".join(context.args)
    search_results = web_search(query)
    
    update.message.reply_text(search_results, parse_mode="Markdown")

# About command handler (optional)
def about(update: Update, context: CallbackContext):
    update.message.reply_text("This is an AI-powered bot. You can ask me anything and I will try to help you. 🤖")

if __name__ == "__main__":
    main()
