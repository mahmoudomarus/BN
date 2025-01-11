from market_data import MarketDataAdapter, MarketAnalyzer
from social_monitor import InfluencerTracker, WebContentAnalyzer, TextFileAnalyzer
from typing import Dict, List, Optional
import json
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DecisionEngine:
    """Advanced decision engine for crypto market analysis"""
    
    def __init__(self):
        logging.debug("Initializing DecisionEngine")
        self.market_data = MarketDataAdapter()
        self.market_analyzer = MarketAnalyzer()
        self.influencer_tracker = InfluencerTracker()
        self.web_analyzer = WebContentAnalyzer()
        self.text_analyzer = TextFileAnalyzer()
        self.analysis_cache = {}
        
    async def analyze_market_conditions(self, coin_id: str) -> Dict:
        logging.debug(f"Analyzing market conditions asynchronously for: {coin_id}")
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'market_data': {},
            'social_signals': {},
            'technical_indicators': {},
            'risk_assessment': {},
            'decision_factors': []
        }
        
        # Get market data
        market_data = self.market_data.get_market_data(coin_id)
        if market_data:
            logging.debug(f"Market data retrieved for {coin_id}: {market_data}")
            analysis['market_data'] = {
                'price': market_data.get('market_data', {}).get('current_price', {}).get('usd'),
                'volume': market_data.get('market_data', {}).get('total_volume', {}).get('usd'),
                'market_cap': market_data.get('market_data', {}).get('market_cap', {}).get('usd')
            }
            
        # Track influencer activity
        for influencer in self.influencer_tracker.INFLUENCERS:
            posts = self.influencer_tracker.get_recent_posts(influencer)
            impact = self.influencer_tracker.analyze_impact(posts, coin_id)
            if impact['impact_score'] > 0:
                logging.debug(f"Influencer impact detected: {impact}")
                analysis['social_signals'][influencer] = impact
                
        # Risk assessment
        analysis['risk_assessment'] = self.assess_risk(market_data, analysis['social_signals'])
        logging.debug(f"Risk assessment completed: {analysis['risk_assessment']}")
        
        return analysis
        
    def analyze_market_conditions_sync(self, coin_id: str) -> Dict:
        logging.debug(f"Analyzing market conditions synchronously for: {coin_id}")
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'market_data': {},
            'social_signals': {},
            'technical_indicators': {},
            'risk_assessment': {},
            'decision_factors': []
        }
        
        # Get market data
        market_data = self.market_data.get_market_data(coin_id)
        if market_data:
            logging.debug(f"Market data retrieved for {coin_id}: {market_data}")
            analysis['market_data'] = {
                'price': market_data.get('market_data', {}).get('current_price', {}).get('usd'),
                'volume': market_data.get('market_data', {}).get('total_volume', {}).get('usd'),
                'market_cap': market_data.get('market_data', {}).get('market_cap', {}).get('usd')
            }
            
        # Track influencer activity
        for influencer in self.influencer_tracker.INFLUENCERS:
            posts = self.influencer_tracker.get_recent_posts(influencer)
            impact = self.influencer_tracker.analyze_impact(posts, coin_id)
            if impact['impact_score'] > 0:
                logging.debug(f"Influencer impact detected: {impact}")
                analysis['social_signals'][influencer] = impact
                
        # Risk assessment
        analysis['risk_assessment'] = self.assess_risk(market_data, analysis['social_signals'])
        logging.debug(f"Risk assessment completed: {analysis['risk_assessment']}")
        
        return analysis
        
    def assess_risk(self, market_data: Dict, social_signals: Dict) -> Dict:
        logging.debug("Assessing risk factors")
        risk_assessment = {
            'market_risk': 0,
            'social_risk': 0,
            'volatility_risk': 0,
            'overall_risk': 0,
            'risk_factors': []
        }
        
        # Market risk factors
        if market_data:
            price_change = market_data.get('market_data', {}).get('price_change_percentage_24h', 0)
            volume = market_data.get('market_data', {}).get('total_volume', {}).get('usd', 0)
            market_cap = market_data.get('market_data', {}).get('market_cap', {}).get('usd', 0)
            
            if abs(price_change) > 20:
                risk_assessment['volatility_risk'] += 2
                risk_assessment['risk_factors'].append('High price volatility')
                
            if volume > 0 and market_cap > 0:
                volume_to_mcap = volume / market_cap
                if volume_to_mcap > 0.5:
                    risk_assessment['market_risk'] += 1
                    risk_assessment['risk_factors'].append('High volume relative to market cap')
                    
        # Social risk factors
        for influencer, impact in social_signals.items():
            if impact['impact_score'] > 5:
                risk_assessment['social_risk'] += 1
                risk_assessment['risk_factors'].append(f'High social impact from {influencer}')
                
        # Calculate overall risk
        risk_assessment['overall_risk'] = (
            risk_assessment['market_risk'] + 
            risk_assessment['social_risk'] + 
            risk_assessment['volatility_risk']
        ) / 3
        
        logging.debug(f"Risk assessment completed: {risk_assessment}")
        return risk_assessment
        
    def generate_decision_report(self, analysis: Dict) -> str:
        logging.debug("Generating decision report")
        report = []
        
        report.append("=== Market Analysis Report ===")
        report.append(f"Generated at: {analysis['timestamp']}")
        report.append("\n=== Market Data ===")
        for key, value in analysis['market_data'].items():
            report.append(f"{key}: {value}")
            
        report.append("\n=== Social Signals ===")
        for influencer, signals in analysis['social_signals'].items():
            report.append(f"\nInfluencer: {influencer}")
            report.append(f"Impact Score: {signals['impact_score']}")
            report.append(f"Relevant Posts: {len(signals['relevant_posts'])}")
            
        report.append("\n=== Risk Assessment ===")
        risk = analysis['risk_assessment']
        report.append(f"Overall Risk: {risk['overall_risk']:.2f}")
        report.append("Risk Factors:")
        for factor in risk['risk_factors']:
            report.append(f"- {factor}")
            
        logging.debug("Decision report generated")
        return "\n".join(report)
        
    def process_text_file(self, file_path: str, keywords: List[str]) -> Dict:
        logging.debug(f"Processing text file: {file_path}")
        content = self.text_analyzer.read_file(file_path)
        if content:
            return self.text_analyzer.analyze_content(content, keywords)
        logging.debug(f"Text file processing failed: {file_path}")
        return {}
        
    def analyze_webpage(self, url: str, keywords: List[str]) -> Dict:
        logging.debug(f"Analyzing webpage: {url}")
        content = self.web_analyzer.fetch_webpage(url)
        if content:
            return self.web_analyzer.analyze_webpage(content, keywords)
        logging.debug(f"Webpage analysis failed: {url}")
        return {}