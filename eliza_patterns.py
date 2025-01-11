from typing import Dict, List, Tuple, Optional
import re
import random

# Market-specific decomposition rules
MARKET_PATTERNS = {
    'price_patterns': [
        (r'what.*price.*(of|for)\s+(\w+)', 'price_inquiry'),
        (r'how much.*(\w+).*worth', 'price_inquiry'),
        (r'(\w+).*price.*analysis', 'price_analysis')
    ],
    'trend_patterns': [
        (r'(.*)(pumping|dumping|mooning)', 'trend_analysis'),
        (r'why.*(\w+).*(up|down)', 'trend_reasoning'),
        (r'what.*happening.*(\w+)', 'market_update')
    ],
    'social_patterns': [
        (r'.*elon.*tweet.*(\w+)', 'influencer_impact'),
        (r'what.*people.*saying.*(\w+)', 'social_sentiment'),
        (r'.*community.*(\w+)', 'community_analysis')
    ]
}

# Response templates
RESPONSE_TEMPLATES = {
    'price_inquiry': [
        "What makes you interested in {coin}'s price right now?",
        "How long have you been tracking {coin}'s price movements?",
        "What price level are you watching for {coin}?"
    ],
    'trend_analysis': [
        "What indicators suggest this trend in {coin}?",
        "Have you noticed any patterns in {coin}'s movements?",
        "What timeframe are you analyzing for {coin}?"
    ],
    'influencer_impact': [
        "How do you think this will affect {coin}'s market?",
        "What's your analysis of the influencer's impact on {coin}?",
        "Have you seen similar patterns with {coin} before?"
    ]
}

def match_crypto_pattern(user_input: str) -> Optional[Tuple[str, Dict]]:
    """Enhanced pattern matching for crypto-specific queries"""
    for pattern_type, patterns in MARKET_PATTERNS.items():
        for pattern, response_type in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                groups = match.groups()
                coin = groups[-1] if groups else ""
                return (
                    random.choice(RESPONSE_TEMPLATES.get(response_type, ["Tell me more about that."])),
                    {'coin': coin}
                )
    return None