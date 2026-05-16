# System Architecture

```
flowchart TD
    A[User] --> B[Streamlit/Flask UI]
    B --> C[Orchestrator]
    C --> D[NewsAgent]
    C --> E[TrendsAgent]
    C --> F[DataAgent]
    D --> G[NewsAPI/Web Sources]
    E --> H[YFinance]
    F --> I[Real-time Data]
    C --> J[InsightsAgent]
    J --> K[Gemini Pro]
    J --> L[PortfolioAdvisor]
```

## Tech Stack
- **Agents**: Google ADK
- **AI**: Vertex AI (Gemini Pro)
- **Cloud**: Cloud Run, Cloud Build
- **Data**: Yahoo Finance, NewsAPI
```

**3. tests/test_agents.py**
```python
import pytest
from agents import NewsAgent, DataAgent

def test_news_agent():
    agent = NewsAgent()
    assert "AAPL" in agent.tickers
    assert isinstance(agent.get_news("AAPL"), str)

def test_data_agent():
    agent = DataAgent()
    price = agent.get_real_time_price("AAPL")
    assert isinstance(price, float)
```

**4. frontend/templates/index.html (Flask Template)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>AI Stock Analyst</title>
</head>
<body>
    <h1>Stock Analysis for {{ ticker }}</h1>
    <p>{{ recommendation }}</p>
</body>
</html>
```

**5. frontend/app.py (Flask Alternative)**
```python
from flask import Flask, render_template, request
from orchestration.main_adk import StockAnalysisOrchestrator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        orchestrator = StockAnalysisOrchestrator()
        recommendation = orchestrator.analyze_ticker(ticker)
        return render_template('index.html', 
               ticker=ticker, 
               recommendation=recommendation)
    return render_template('index.html')
```

**6. tests/__init__.py**
```python
# Initialize tests package
```

**7. .env.example**
```
TICKERS="AAPL,GOOGL,MSFT"
GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
ALPHA_VANTAGE_KEY="your_key_here"
```

**Key Collaboration Features:**
1. **Modular Design**: Each agent can be developed independently
2. **Shared Interfaces**: Agents use standardized input/output formats
3. **Cross-Platform Testing**: Includes both Streamlit and Flask options
4. **CI/CD Ready**: cloudbuild.yaml automates deployment
5. **Mock Data Support**: Tests include sample data validation

**To Get Started:**
1. Copy these files to corresponding locations
2. Run `pip install -r requirements.txt`
3. For Flask version:
   ```powershell
   $env:FLASK_APP = "frontend/app.py"
   flask run
   ```
4. For Streamlit:
   ```powershell
   streamlit run frontend/app.py
   ```

**Pro Tip:** Use this collaboration workflow:
1. Saurabh focuses on `DataAgent` and `TrendsAgent`
2. Luis develops `InsightsAgent` and `PortfolioAdvisor`
3. Daily merge conflicts resolution using:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git merge main
   ```


