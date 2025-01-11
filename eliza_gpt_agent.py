import re
import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Basic ELIZA patterns and responses
ELIZA_PATTERNS = {
    r'I need (.*?)': [
        "Why do you need {}?",
        "Would it really help you to get {}?",
        "Are you sure you need {}?"
    ],
    r'I am (.*?)': [
        "Did you come to me because you are {}?",
        "How long have you been {}?",
        "How do you feel about being {}?"
    ],
    r'I\'m (.*?)': [
        "How does being {} make you feel?",
        "Do you enjoy being {}?",
        "Why do you tell me you're {}?"
    ],
    r'Are you (.*?)': [
        "Why does it matter whether I am {}?",
        "Would you prefer if I were not {}?",
        "Perhaps you believe I am {}?"
    ],
    r'What (.*?)': [
        "Why do you ask?",
        "How would an answer to that help you?",
        "What do you think?"
    ],
    r'How (.*?)': [
        "How do you suppose?",
        "Perhaps you can answer your own question?",
        "What is it you're really asking?"
    ],
    r'Because (.*)': [
        "Is that the real reason?",
        "What other reasons might there be?",
        "Does that reason explain anything else?"
    ],
    r'(.*?) sorry (.*?)': [
        "There are many times when no apology is needed.",
        "What feelings do you have when you apologize?",
        "Don't be sorry - just tell me more."
    ],
    r'(.*?) friend (.*?)': [
        "Tell me more about your friends.",
        "When you think of a friend, what comes to mind?",
        "Why don't you tell me about a childhood friend?"
    ],
    r'Yes': [
        "You seem quite sure.",
        "OK, but can you elaborate a bit?",
        "Can you tell me more about that?"
    ],
    r'No': [
        "Why not?",
        "Can you elaborate on that?",
        "Tell me more about your thinking on this."
    ]
}

def match_eliza_pattern(user_input: str) -> Optional[Tuple[str, str]]:
    """Try to match user input against ELIZA patterns and return a response template."""
    for pattern, responses in ELIZA_PATTERNS.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # Get the matched group if it exists, otherwise use the whole match
            captured = match.group(1) if match.groups() else match.group(0)
            response_template = random.choice(responses)
            return response_template, captured
    return None

def get_gpt_response(user_input: str) -> str:
    """Get a response from GPT when ELIZA patterns don't match."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ELIZA, the classic therapy chatbot. "
                 "Respond in ELIZA's characteristic style: reflective, non-directive, "
                 "and often responding to statements with questions. Keep responses "
                 "short and focused on the user's feelings and thoughts."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"I'm having trouble understanding. Can you rephrase that? (Error: {str(e)})"

def main():
    """Main conversation loop."""
    print("ELIZA-GPT: Hello, I am ELIZA. How are you feeling today?")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nELIZA-GPT: Goodbye. Take care!")
            break
            
        # Try ELIZA patterns first
        eliza_match = match_eliza_pattern(user_input)
        
        if eliza_match:
            response_template, captured = eliza_match
            try:
                response = response_template.format(captured)
            except:
                response = response_template
            print(f"\nELIZA-GPT: {response}")
        else:
            # Fallback to GPT
            gpt_response = get_gpt_response(user_input)
            print(f"\nELIZA-GPT: {gpt_response}")

if __name__ == "__main__":
    main()
