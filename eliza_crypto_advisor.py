import re
import random
from typing import Dict, List, Tuple, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class CryptoAdvisor:
    def __init__(self):
        # Initialize the model and tokenizer
        self.model_name = "facebook/opt-350m"  # Using a smaller model for faster responses
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Initialize patterns
        self.init_patterns()

    def init_patterns(self):
        """Initialize ELIZA-style patterns for crypto analysis"""
        self.CRYPTO_PATTERNS = {
            r'.*?\b(price|value|worth)\b.*?(\w+)': [
                "What factors do you think are affecting {}'s price?",
                "Have you noticed any patterns in {}'s price movements?",
                "What timeframe are you analyzing for {}?"
            ],
            r'.*?\b(analyze|analysis)\b.*?(\w+)': [
                "Let's look at {}. What specific aspects interest you?",
                "What indicators would you like to analyze for {}?",
                "How long have you been tracking {}?"
            ],
            r'.*?\b(trend|trending)\b.*?(\w+)': [
                "What makes you interested in {}'s trends?",
                "Have you noticed any specific patterns in {}'s movement?",
                "What timeframe are you looking at for {}?"
            ],
            r'.*?\b(risk|safe|danger)\b.*?(\w+)': [
                "What specific risks are you concerned about with {}?",
                "How do you usually assess risk for tokens like {}?",
                "What's your risk management strategy for {}?"
            ],
            r'.*?\b(community|social)\b.*?(\w+)': [
                "What aspects of {}'s community interest you?",
                "How do you gauge {}'s social sentiment?",
                "What community metrics do you track for {}?"
            ]
        }

def match_pattern(user_input: str) -> Optional[Tuple[str, str]]:
    """Match user input against crypto-specific patterns"""
    advisor = CryptoAdvisor()
    for pattern, responses in advisor.CRYPTO_PATTERNS.items():
        match = re.search(pattern, user_input.lower())
        if match:
            # Get the captured coin name or use the whole match
            captured = match.group(2) if len(match.groups()) > 1 else match.group(1)
            response_template = random.choice(responses)
            return response_template, captured
    return None

def get_market_aware_response(user_input: str) -> str:
    """Generate a response using the language model"""
    advisor = CryptoAdvisor()
    try:
        # Prepare the prompt
        prompt = f"You are a crypto market analyst. Respond to: {user_input}"
        
        # Encode and generate response
        inputs = advisor.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = advisor.model.generate(
            inputs,
            max_length=150,
            num_return_sequences=1,
            pad_token_id=advisor.tokenizer.eos_token_id,
            temperature=0.7
        )
        
        # Decode and clean up response
        response = advisor.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the actual response (remove the prompt)
        response = response.replace(prompt, "").strip()
        
        return response if response else "Could you clarify what you'd like to know about the crypto market?"
    
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I'm having trouble analyzing that. Could you rephrase your question?"

if __name__ == "__main__":
    # Test the pattern matching
    test_input = "analyze BTC price trends"
    pattern_match = match_pattern(test_input)
    if pattern_match:
        response_template, captured = pattern_match
        print(f"Pattern match: {response_template.format(captured)}")
    else:
        print("No pattern match, using AI response:")
        print(get_market_aware_response(test_input))