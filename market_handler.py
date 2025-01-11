import aiohttp
import asyncio
from typing import Dict, Optional, List
import json
from datetime import datetime, timedelta

class MarketDataHandler:
    def __init__(self):
        self.coingecko_api = "https://api.coingecko.com/api/v3"
        self.cache = {}
        self.cache_duration = 60  # seconds

    async def get_coin_data(self, coin_id: str) -> Optional[Dict]:
        """Fetch comprehensive coin data from CoinGecko"""
        try:
            url = f"{self.coingecko_api}/coins/{coin_id}"
            params = {
                "localization": "false",
                "tickers": "true",
                "market_data": "true",
                "community_data": "true",
                "developer_data": "true",
                "sparkline": "true"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            print(f"Error fetching coin data: {str(e)}")
        return None

    async def get_market_analysis(self, coin_id: str) -> Dict:
        """Get comprehensive market analysis"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'price_data': {},
            'market_metrics': {},
            'social_metrics': {},
            'trading_signals': [],
            'risk_analysis': {}
        }
        
        coin_data = await self.get_coin_data(coin_id)
        if not coin_data:
            return data

        # Price Data
        market_data = coin_data.get('market_data', {})
        data['price_data'] = {
            'current_price': market_data.get('current_price', {}).get('usd'),
            'price_change_24h': market_data.get('price_change_percentage_24h'),
            'price_change_7d': market_data.get('price_change_percentage_7d'),
            'price_change_30d': market_data.get('price_change_percentage_30d'),
            'ath': market_data.get('ath', {}).get('usd'),
            'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd')
        }

        # Market Metrics
        data['market_metrics'] = {
            'market_cap': market_data.get('market_cap', {}).get('usd'),
            'market_cap_rank': coin_data.get('market_cap_rank'),
            'total_volume': market_data.get('total_volume', {}).get('usd'),
            'circulating_supply': market_data.get('circulating_supply'),
            'total_supply': market_data.get('total_supply')
        }

        # Social Metrics
        community_data = coin_data.get('community_data', {})
        data['social_metrics'] = {
            'twitter_followers': community_data.get('twitter_followers'),
            'reddit_subscribers': community_data.get('reddit_subscribers'),
            'reddit_active_accounts': community_data.get('reddit_active_accounts'),
            'telegram_channel_user_count': community_data.get('telegram_channel_user_count')
        }

        # Trading Signals
        volume_change = market_data.get('volume_change_24h', 0)
        price_change = market_data.get('price_change_percentage_24h', 0)
        
        if volume_change and price_change:
            if volume_change > 20 and price_change > 0:
                data['trading_signals'].append("High volume with price increase - potential bullish signal")
            elif volume_change > 20 and price_change < 0:
                data['trading_signals'].append("High volume with price decrease - potential bearish signal")

        # Risk Analysis
        volume_to_mcap = data['market_metrics']['total_volume'] / data['market_metrics']['market_cap'] if data['market_metrics']['market_cap'] else 0
        
        data['risk_analysis'] = {
            'volatility_24h': abs(price_change) if price_change else 0,
            'volume_to_mcap_ratio': volume_to_mcap,
            'risk_level': self._calculate_risk_level(price_change, volume_to_mcap, market_data)
        }

        return data

    def _calculate_risk_level(self, price_change: float, volume_to_mcap: float, market_data: Dict) -> str:
        risk_score = 0
        
        # Price volatility risk
        if abs(price_change) > 20:
            risk_score += 3
        elif abs(price_change) > 10:
            risk_score += 2
        elif abs(price_change) > 5:
            risk_score += 1

        # Volume to market cap risk
        if volume_to_mcap > 0.3:
            risk_score += 3
        elif volume_to_mcap > 0.1:
            risk_score += 1

        # Market cap risk
        market_cap = market_data.get('market_cap', {}).get('usd', 0)
        if market_cap < 100000000:  # Less than 100M
            risk_score += 3
        elif market_cap < 1000000000:  # Less than 1B
            risk_score += 2

        if risk_score >= 7:
            return "Very High"
        elif risk_score >= 5:
            return "High"
        elif risk_score >= 3:
            return "Medium"
        else:
            return "Low"

    async def get_social_impact(self, coin_id: str) -> Dict:
        """Analyze social media impact"""
        data = await self.get_coin_data(coin_id)
        if not data:
            return {}

        community_data = data.get('community_data', {})
        public_interest_stats = data.get('public_interest_stats', {})

        return {
            'social_score': data.get('coingecko_score'),
            'community_score': data.get('community_score'),
            'social_metrics': {
                'twitter_followers': community_data.get('twitter_followers'),
                'reddit_subscribers': community_data.get('reddit_subscribers'),
                'telegram_users': community_data.get('telegram_channel_user_count')
            },
            'public_interest': public_interest_stats.get('alexa_rank')
        }