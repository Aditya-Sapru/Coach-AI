# nutritionist_agent.py
import os
import requests
from dotenv import load_dotenv
from user_profile import load_user_profile
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

def get_initial_prompt():
    user_data = load_user_profile()
    return (
        "You are a professional nutritionist. Your role is to:\n"
        "1. Help users achieve their fitness goals through proper nutrition\n"
        "2. Create personalized meal plans based on user data and preferences\n"
        "3. Consider dietary restrictions, allergies, and food preferences\n"
        "4. Calculate and track macronutrients and calories\n"
        "5. Provide scientific explanations for your recommendations\n"
        "6. Be conversational and ask for confirmations\n\n"
        f"You are working with {user_data.get('name', 'a user')} who is {user_data.get('age', '')} years old, "
        f"{user_data.get('gender', '')}, weighing {user_data.get('weight', '')}kg, {user_data.get('height', '')}cm tall, "
        f"with {user_data.get('experience_level', 'beginner')} experience level in fitness. "
        "Calculate their BMR and TDEE to provide accurate caloric recommendations. "
        "Always maintain a professional yet friendly tone."
    )

# Chat history for maintaining context
conversation_history = [
    {
        "role": "user",
        "parts": [{"text": get_initial_prompt()}]
    }
]

def send_to_nutritionist(user_input):
    # Add user input to history
    conversation_history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": conversation_history
    }

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        # Save model response to history
        conversation_history.append({
            "role": "model",
            "parts": [{"text": reply}]
        })
        return reply
    except Exception as e:
        return f"Error: {str(e)}"

def get_meal_plan(messages):
    """
    Generate a meal plan using the Gemini API.
    messages: List of message dictionaries with 'role' and 'content'
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[])
        
        # Add all messages to the chat
        for message in messages:
            if message['role'] == 'user':
                response = chat.send_message(message['content'])
            elif message['role'] == 'system':
                # For system messages, we'll incorporate them into the context
                chat.send_message(f"System: {message['content']}")
        
        # Get the last response
        return response.text
    except Exception as e:
        return f"Error generating meal plan: {str(e)}"

def clear_conversation():
    """Clear the conversation history except for the system prompt"""
    global conversation_history
    conversation_history = [
        {
            "role": "user",
            "parts": [{"text": get_initial_prompt()}]
        }
    ]
