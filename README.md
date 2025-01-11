# BN - ElizaAI Two

A crypto market analysis tool powered by ELIZA-style pattern matching and HuggingFace Transformers. This tool provides real-time market analysis, social media sentiment tracking, and technical analysis without relying on paid APIs.

## Features

- 🤖 AI-powered market analysis
- 📊 Real-time crypto market data
- 📱 Social media sentiment tracking
- 👥 Influencer activity monitoring
- 📈 Technical analysis and pattern recognition
- ⚠️ Risk assessment
- 🔄 Market trend analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/mahmoudomarus/BN.git
cd BN

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Run Streamlit App
```bash
streamlit run streamlit_app.py
```

### Run Web Interface
```bash
python app.py
```

## Project Structure

```
BN/
├── app.py                  # Flask web application
├── streamlit_app.py        # Streamlit interface
├── eliza_crypto_advisor.py # Core ELIZA implementation
├── market_data.py         # Market data handler
├── social_monitor.py      # Social media monitoring
└── requirements.txt       # Project dependencies
```

## Usage Example

1. Start the application
2. Enter queries like:
   - "analyze DOGE coin"
   - "check BTC trends"
   - "show ETH social sentiment"
3. Get real-time analysis with:
   - Price data
   - Market metrics
   - Social sentiment
   - Risk analysis

## Technologies Used

- Python
- Streamlit
- HuggingFace Transformers
- Flask
- Plotly
- Technical Analysis Libraries