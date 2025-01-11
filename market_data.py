import requests
import json
from typing import Dict, Optional
from datetime import datetime
import pandas as pd

class MarketDataHandler:
    def __init__(self):
        self.coingecko_api = "https://api.coingecko.com/api/v3"
        self.cache = {}
        self.cache_duration = 60  # seconds

    def get_coin_data(self, coin_id: str) -> Optional[Dict]:
        """Fetch current coin data from CoinGecko"""
        try:
            url = f"{self.coingecko_api}/coins/{coin_id}"
            params = {
                "localization": "false",
                "tickers": "true",
                "market_data": "true",
                "community_data": "true",
                "developer_data": "true"
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching coin data: {str(e)}")
            return None

    def get_market_analysis_sync(self, coin_id: str) -> Dict:
        """Get comprehensive market analysis"""
        try:
            coin_data = self.get_coin_data(coin_id)
            if not coin_data:
                return self.get_default_analysis()

            market_data = coin_data.get('market_data', {})
            community_data = coin_data.get('community_data', {})

            analysis = {
                'timestamp': datetime.now().isoformat(),
                'price_data': {
                    'current_price': market_data.get('current_price', {}).get('usd'),
                    'price_change_24h': market_data.get('price_change_percentage_24h'),
                    'price_change_7d': market_data.get('price_change_percentage_7d'),
                    'ath': market_data.get('ath', {}).get('usd'),
                    'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd')
                },
                'market_metrics': {
                    'market_cap': market_data.get('market_cap', {}).get('usd'),
                    'market_cap_rank': coin_data.get('market_cap_rank'),
                    'total_volume': market_data.get('total_volume', {}).get('usd'),
                    'circulating_supply': market_data.get('circulating_supply'),
                    'total_supply': market_data.get('total_supply')
                },
                'social_metrics': {
                    'twitter_followers': community_data.get('twitter_followers'),
                    'reddit_subscribers': community_data.get('reddit_subscribers'),
                    'telegram_channel_user_count': community_data.get('telegram_channel_user_count')
                },
                'risk_analysis': self.calculate_risk_metrics(market_data),
                'trading_signals': self.generate_trading_signals(market_data)
            }
            return analysis
        except Exception as e:
            print(f"Error in market analysis: {str(e)}")
            return self.get_default_analysis()

    def get_default_analysis(self) -> Dict:
        """Return default analysis structure with null values"""
        return {
            'timestamp': datetime.now().isoformat(),
            'price_data': {
                'current_price': None,
                'price_change_24h': None,
                'price_change_7d': None,
                'ath': None,
                'ath_change_percentage': None
            },
            'market_metrics': {
                'market_cap': None,
                'market_cap_rank': None,
                'total_volume': None,
                'circulating_supply': None,
                'total_supply': None
            },
            'social_metrics': {
                'twitter_followers': None,
                'reddit_subscribers': None,
                'telegram_channel_user_count': None
            },
            'risk_analysis': {
                'risk_level': 'Unknown',
                'volatility_24h': None
            },
            'trading_signals': []
        }

    def calculate_risk_metrics(self, market_data: Dict) -> Dict:
        """Calculate risk metrics from market data"""
        risk_metrics = {
            'risk_level': 'Medium',
            'volatility_24h': abs(market_data.get('price_change_percentage_24h', 0))
        }

        # Adjust risk level based on volatility
        if risk_metrics['volatility_24h'] > 20:
            risk_metrics['risk_level'] = 'High'
        elif risk_metrics['volatility_24h'] < 5:
            risk_metrics['risk_level'] = 'Low'

        return risk_metrics

    def generate_trading_signals(self, market_data: Dict) -> list:
        """Generate trading signals based on market data"""
        signals = []
        price_change = market_data.get('price_change_percentage_24h', 0)
        volume_change = market_data.get('volume_change_24h', 0)

        if abs(price_change) > 10:
            signals.append(f"High volatility detected: {price_change:.1f}% price change in 24h")

        if volume_change > 50:
            signals.append(f"Significant volume increase: {volume_change:.1f}% in 24h")
        elif volume_change < -50:
            signals.append(f"Significant volume decrease: {volume_change:.1f}% in 24h")

        return signals