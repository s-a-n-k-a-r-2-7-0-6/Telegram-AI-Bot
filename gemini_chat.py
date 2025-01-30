import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Correct model name usage
def get_gemini_response(user_message):
    try:
        model = genai.GenerativeModel("gemini-pro")  # Ensure correct model
        response = model.generate_content(user_message)
        return response.text if response else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
