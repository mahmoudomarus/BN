import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class InfluencerTracker:
    """Tracks crypto influencers and their market impact without using tweepy"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
        # Define key influencers and their typical impact
        self.INFLUENCERS = {
            'elonmusk': {
                'impact_score': 9.5,
                'keywords': ['doge', 'crypto', 'bitcoin', 'btc'],
                'platform': 'twitter'
            },
            'VitalikButerin': {
                'impact_score': 8.5,
                'keywords': ['ethereum', 'eth', 'layer2', 'scaling'],
                'platform': 'twitter'
            },
            'cz_binance': {
                'impact_score': 8.0,
                'keywords': ['bnb', 'binance', 'listing', 'trading'],
                'platform': 'twitter'
            },
            'saylor': {
                'impact_score': 8.0,
                'keywords': ['bitcoin', 'btc', 'crypto'],
                'platform': 'twitter'
            }
        }

    def get_social_metrics(self, coin_id: str) -> Dict:
        """Get social metrics from CoinGecko"""
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "false",
                "community_data": "true",
                "developer_data": "false"
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                community_data = data.get('community_data', {})
                return {
                    'twitter_followers': community_data.get('twitter_followers', 0),
                    'reddit_subscribers': community_data.get('reddit_subscribers', 0),
                    'telegram_channel_user_count': community_data.get('telegram_channel_user_count', 0),
                    'reddit_active_accounts': community_data.get('reddit_average_posts_48h', 0)
                }
        except Exception as e:
            print(f"Error fetching social metrics: {str(e)}")
        return self.get_default_metrics()

    def get_default_metrics(self) -> Dict:
        """Return default metrics when data can't be fetched"""
        return {
            'twitter_followers': 0,
            'reddit_subscribers': 0,
            'telegram_channel_user_count': 0,
            'reddit_active_accounts': 0
        }

    def analyze_social_sentiment(self, coin_id: str) -> Dict:
        """Analyze social sentiment for a coin"""
        metrics = self.get_social_metrics(coin_id)
        
        # Calculate engagement score (simplified)
        total_followers = (
            metrics['twitter_followers'] +
            metrics['reddit_subscribers'] +
            metrics['telegram_channel_user_count']
        )
        
        # Basic sentiment analysis
        sentiment = {
            'overall_score': 0,
            'community_strength': 'low',
            'engagement_level': 'low',
            'potential_signals': []
        }
        
        # Analyze community size
        if total_followers > 1000000:
            sentiment['community_strength'] = 'very high'
            sentiment['overall_score'] += 3
        elif total_followers > 100000:
            sentiment['community_strength'] = 'high'
            sentiment['overall_score'] += 2
        elif total_followers > 10000:
            sentiment['community_strength'] = 'medium'
            sentiment['overall_score'] += 1
            
        # Analyze engagement
        if metrics['reddit_active_accounts'] > 1000:
            sentiment['engagement_level'] = 'very high'
            sentiment['overall_score'] += 3
            sentiment['potential_signals'].append("High community engagement detected")
        elif metrics['reddit_active_accounts'] > 100:
            sentiment['engagement_level'] = 'high'
            sentiment['overall_score'] += 2
            
        return sentiment

    def get_influencer_impact(self, coin_id: str) -> List[Dict]:
        """Get potential influencer impact for a coin"""
        impacts = []
        for influencer, data in self.INFLUENCERS.items():
            if any(keyword in coin_id.lower() for keyword in data['keywords']):
                impacts.append({
                    'influencer': influencer,
                    'platform': data['platform'],
                    'impact_score': data['impact_score'],
                    'relevant_keywords': [k for k in data['keywords'] if k in coin_id.lower()]
                })
        return impacts

    def get_overall_analysis(self, coin_id: str) -> Dict:
        """Get comprehensive social analysis"""
        return {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.get_social_metrics(coin_id),
            'sentiment': self.analyze_social_sentiment(coin_id),
            'influencer_impact': self.get_influencer_impact(coin_id)
        }