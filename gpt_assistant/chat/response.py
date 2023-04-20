import os
import openai


def generate_response(messages):
    """Generate a chat response with ChatGPT"""
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo"),
        messages=messages
    )
    reply = response.choices[0].message.content.strip()
    return reply
