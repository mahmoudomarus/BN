import streamlit as st
from eliza_crypto_advisor import match_pattern, get_market_aware_response
from market_data import MarketDataHandler
from social_monitor import InfluencerTracker
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

# Initialize components
market_handler = MarketDataHandler()
influencer_tracker = InfluencerTracker()

# Page config
st.set_page_config(
    page_title="ElizaAI Two - Crypto Advisor",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("ElizaAI Two - Crypto Market Advisor")
st.markdown("""
This AI-powered crypto market advisor helps analyze trends, track influencer activity, 
and monitor market sentiment.
""")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm ElizaAI Two. How can I help you analyze the crypto market today?"
    })

# Create two columns
col1, col2 = st.columns([3, 2])

with col1:
    # Chat interface
    st.subheader("Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about market trends, tokens, or analysis..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        pattern_match = match_pattern(prompt)
        if pattern_match:
            response_template, captured = pattern_match
            try:
                response = response_template.format(captured)
            except:
                response = response_template
        else:
            response = get_market_aware_response(prompt)
        
        # Add AI response
        st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    # Market Monitor
    st.subheader("Market Monitor")
    
    # Get current analysis if available
    try:
        analysis = market_handler.get_market_analysis_sync('bitcoin')  # Default to Bitcoin
        
        # Price metrics
        st.metric(
            label="Current Price",
            value=f"${analysis['price_data']['current_price']:,.2f}",
            delta=f"{analysis['price_data']['price_change_24h']:.2f}%"
        )
        
        # Market metrics
        with st.expander("Market Metrics"):
            cols = st.columns(2)
            with cols[0]:
                st.metric("Market Cap", f"${analysis['market_metrics']['market_cap']:,.0f}")
            with cols[1]:
                st.metric("24h Volume", f"${analysis['market_metrics']['total_volume']:,.0f}")
        
        # Social metrics
        st.subheader("Influencer Activity")
        with st.expander("Social Metrics"):
            social = analysis['social_metrics']
            cols = st.columns(3)
            with cols[0]:
                st.metric("Twitter", f"{social['twitter_followers']:,}")
            with cols[1]:
                st.metric("Reddit", f"{social['reddit_subscribers']:,}")
            with cols[2]:
                st.metric("Telegram", f"{social['telegram_channel_user_count']:,}")
        
        # Analysis results
        st.subheader("Analysis Results")
        with st.expander("Risk Analysis"):
            st.write(f"Risk Level: {analysis['risk_analysis']['risk_level']}")
            st.write(f"Volatility: {analysis['risk_analysis']['volatility_24h']:.2f}%")
            
            if analysis['trading_signals']:
                st.write("Trading Signals:")
                for signal in analysis['trading_signals']:
                    st.write(f"• {signal}")
                    
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and HuggingFace Transformers")
