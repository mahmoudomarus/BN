import re
import os
import random
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables at the start
load_dotenv(override=True)

# Initialize OpenAI client with explicit error handling
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables")

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    raise

# Placeholder for ElizaOS pattern matching logic
# This should be replaced with actual logic from ElizaOS

def match_pattern(user_input: str) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    # Example pattern logic
    if "doge" in user_input.lower():
        return "What do you think about Dogecoin?", {}
    elif "bitcoin" in user_input.lower():
        return "Bitcoin is quite volatile these days.", {}
    # Add more patterns as needed
    return None, None

def get_market_aware_response(user_input: str) -> str:
    """Get a response from GPT with market context."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a knowledgeable crypto market analyst. 
                Focus on analyzing trends and patterns. Provide analytical insights but never 
                direct financial advice. Ask questions to better understand the user's 
                analytical needs."""},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"I encountered an error processing your request. Error: {str(e)}"

# Test the OpenAI connection
if __name__ == "__main__":
    try:
        response = get_market_aware_response("Test message")
        print("OpenAI connection successful")
    except Exception as e:
        print(f"Error testing OpenAI connection: {str(e)}")
