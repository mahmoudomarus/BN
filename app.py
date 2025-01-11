from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from eliza_patterns import match_crypto_pattern
from market_handler import MarketDataHandler
from eliza_crypto_advisor import get_market_aware_response
import os
from dotenv import load_dotenv
import asyncio
import json
from datetime import datetime
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize handlers
market_handler = MarketDataHandler()

# HTML Template (keeping your existing template)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Crypto Market Advisor</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .chat-container { height: calc(100vh - 300px); }
        .market-data { height: 200px; overflow-y: auto; }
        .message { margin: 10px; padding: 10px; border-radius: 10px; }
        .user-message { background-color: #3b82f6; color: white; margin-left: 20%; }
        .bot-message { background-color: #f3f4f6; margin-right: 20%; }
        .analysis-panel { height: 300px; overflow-y: auto; }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Chat Interface -->
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h1 class="text-2xl font-bold mb-4">Crypto Market Advisor</h1>
                <div id="chat-container" class="chat-container mb-4"></div>
                <form id="chat-form" class="flex gap-2">
                    <input type="text" 
                           id="user-input" 
                           class="flex-1 p-2 border rounded-lg"
                           placeholder="Ask about market trends, tokens, or analysis...">
                    <button type="submit" 
                            class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
                        Send
                    </button>
                </form>
            </div>
            
            <!-- Market Monitor -->
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h2 class="text-xl font-bold mb-4">Market Monitor</h2>
                <div id="market-data" class="market-data"></div>
                
                <h3 class="text-lg font-bold mt-4 mb-2">Influencer Activity</h3>
                <div id="influencer-feed" class="analysis-panel"></div>
                
                <h3 class="text-lg font-bold mt-4 mb-2">Analysis Results</h3>
                <div id="analysis-results" class="analysis-panel"></div>
            </div>
        </div>
    </div>
    
    <script>
        const chatContainer = document.getElementById('chat-container');
        const chatForm = document.getElementById('chat-form');
        const userInput = document.getElementById('user-input');
        
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function updateUI(data) {
            if (data.market_data) {
                // Update Market Monitor
                document.getElementById('market-data').innerHTML = `
                    <div class="p-4 border-b">
                        <div class="flex justify-between items-center mb-4">
                            <span class="font-bold text-lg">${data.market_data.coin}</span>
                            <span class="text-xl">$${data.market_data.price_data.current_price?.toLocaleString() || 'N/A'}</span>
                        </div>
                        <div class="grid grid-cols-2 gap-2 text-sm">
                            <div>24h Change: <span class="${data.market_data.price_data.price_change_24h >= 0 ? 'text-green-500' : 'text-red-500'}">
                                ${data.market_data.price_data.price_change_24h?.toFixed(2)}%
                            </span></div>
                            <div>Volume: $${data.market_data.market_metrics.total_volume?.toLocaleString() || 'N/A'}</div>
                            <div>Market Cap: $${data.market_data.market_metrics.market_cap?.toLocaleString() || 'N/A'}</div>
                            <div>Rank: #${data.market_data.market_metrics.market_cap_rank || 'N/A'}</div>
                        </div>
                    </div>
                `;

                // Update Influencer Activity
                document.getElementById('influencer-feed').innerHTML = `
                    <div class="p-4">
                        <div class="mb-4">
                            <div class="font-bold mb-2">Social Metrics</div>
                            <div class="grid grid-cols-2 gap-2 text-sm">
                                <div>Twitter Followers: ${data.market_data.social_metrics.twitter_followers?.toLocaleString() || 'N/A'}</div>
                                <div>Reddit Members: ${data.market_data.social_metrics.reddit_subscribers?.toLocaleString() || 'N/A'}</div>
                                <div>Telegram Users: ${data.market_data.social_metrics.telegram_channel_user_count?.toLocaleString() || 'N/A'}</div>
                            </div>
                        </div>
                    </div>
                `;

                // Update Analysis Results
                document.getElementById('analysis-results').innerHTML = `
                    <div class="p-4">
                        <div class="mb-4">
                            <div class="font-bold mb-2">Risk Analysis</div>
                            <div class="text-sm">
                                <div>Risk Level: <span class="font-bold ${
                                    data.market_data.risk_analysis.risk_level === 'Low' ? 'text-green-500' :
                                    data.market_data.risk_analysis.risk_level === 'Medium' ? 'text-yellow-500' :
                                    'text-red-500'
                                }">${data.market_data.risk_analysis.risk_level || 'N/A'}</span></div>
                                <div>Volatility: ${data.market_data.risk_analysis.volatility_24h?.toFixed(2)}%</div>
                            </div>
                        </div>
                        ${data.market_data.trading_signals.length > 0 ? `
                            <div class="mt-4">
                                <div class="font-bold mb-2">Trading Signals</div>
                                <ul class="list-disc pl-4 text-sm">
                                    ${data.market_data.trading_signals.map(signal => `<li>${signal}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                `;
            }
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = userInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            userInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                const data = await response.json();
                
                if (data.success) {
                    addMessage(data.response);
                    // Update the market data panels
                    updateUI(data);
                } else {
                    addMessage('Sorry, I encountered an error processing your request.');
                }
            } catch (error) {
                addMessage('Sorry, I encountered an error connecting to the server.');
                console.error('Error:', error);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message', '')
        
        # Extract coin name from input (e.g., "DOGE" from "analyze DOGE coin")
        coin_match = re.search(r'(?i)(?:analyze|check|about)\s+(\w+)', user_input)
        coin_id = coin_match.group(1).lower() if coin_match else 'bitcoin'
        
        # Get comprehensive analysis
        analysis = asyncio.run(market_handler.get_market_analysis(coin_id))
        
        # Generate ELIZA-style response
        pattern_match = match_crypto_pattern(user_input)
        if pattern_match:
            template, variables = pattern_match
            response = template.format(**variables)
        else:
            response = get_market_aware_response(user_input)

        # Ensure all required data is present
        market_data = {
            'coin': coin_id.upper(),
            'price_data': analysis.get('price_data', {}),
            'market_metrics': analysis.get('market_metrics', {}),
            'social_metrics': analysis.get('social_metrics', {}),
            'trading_signals': analysis.get('trading_signals', []),
            'risk_analysis': analysis.get('risk_analysis', {})
        }
            
        return jsonify({
            'success': True,
            'response': response,
            'market_data': market_data
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/market-data')
def get_market_data():
    try:
        # Default to Bitcoin if no specific coin is being analyzed
        coin_id = 'bitcoin'
        
        # Get market analysis
        analysis = asyncio.run(market_handler.get_market_analysis(coin_id))
        
        # Get social impact data
        social_impact = asyncio.run(market_handler.get_social_impact(coin_id))
        
        return jsonify({
            'success': True,
            'market_data': analysis.get('price_data'),
            'social_metrics': social_impact.get('social_metrics'),
            'analysis': {
                'risk_analysis': analysis.get('risk_analysis'),
                'trading_signals': analysis.get('trading_signals')
            }
        })
    except Exception as e:
        print(f"Error fetching market data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Advanced Crypto Market Advisor...")
    print("Access the web interface at: http://localhost:5000")
    app.run(debug=True, port=5000)
