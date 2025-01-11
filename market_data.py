import requests
from typing import Dict, List, Optional
import time
import json

class MarketDataAdapter:
    """Handles real-time crypto market data fetching"""
    
    def __init__(self):
        self.coingecko_api = "https://api.coingecko.com/api/v3"
        self.cache = {}
        self.cache_duration = 60  # Cache duration in seconds

    def get_coin_price(self, coin_id: str) -> Optional[float]:
        """Get current price for a specific coin with improved error handling and caching"""
        current_time = time.time()
        # Check cache first
        if coin_id in self.cache and (current_time - self.cache[coin_id]['timestamp'] < self.cache_duration):
            return self.cache[coin_id]['price']
        try:
            response = requests.get(
                f"{self.coingecko_api}/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd"}
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            price = data.get(coin_id, {}).get('usd')
            # Update cache
            self.cache[coin_id] = {'price': price, 'timestamp': current_time}
            return price
        except requests.exceptions.RequestException as e:
            print(f"Error fetching price for {coin_id}: {e}")
            return None

    def get_market_data(self, coin_id: str) -> Dict:
        """Get detailed market data for a coin"""
        try:
            response = requests.get(
                f"{self.coingecko_api}/coins/{coin_id}",
                params={"localization": "false", "tickers": "true", "market_data": "true"}
            )
            return response.json()
        except Exception as e:
            print(f"Error fetching market data: {str(e)}")
            return {}

class SocialMediaMonitor:
    """Monitors social media for crypto-related signals"""
    
    def __init__(self):
        self.nitter_instance = "https://nitter.net"  # Example public Nitter instance
        
    def get_user_tweets(self, username: str) -> List[Dict]:
        """Get recent tweets from a user (using Nitter as example)"""
        try:
            response = requests.get(f"{self.nitter_instance}/{username}/rss")
            # This is a placeholder - in real implementation, would parse RSS feed
            return [{"text": "Example tweet", "timestamp": time.time()}]
        except Exception as e:
            print(f"Error fetching tweets: {str(e)}")
            return []

class MarketAnalyzer:
    """Analyzes market data and social signals"""
    
    def analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (placeholder)"""
        positive_words = {'moon', 'pump', 'bullish', 'buy', 'good', 'great'}
        negative_words = {'dump', 'bearish', 'sell', 'bad', 'crash'}
        
        words = text.lower().split()
        score = sum(1 for word in words if word in positive_words)
        score -= sum(1 for word in words if word in negative_words)
        return score

    def analyze_market_impact(self, pre_price: float, post_price: float) -> float:
        """Calculate price impact percentage"""
        if pre_price == 0:
            return 0
        return ((post_price - pre_price) / pre_price) * 100
