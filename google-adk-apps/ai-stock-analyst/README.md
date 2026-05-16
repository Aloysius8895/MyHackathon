# Ai Stock Analyst
AI Stock Analyst Team is a modern, multi-agent web application that leverages advanced artificial intelligence to deliver comprehensive, real-time stock analysis and investment recommendations. The platform integrates specialized AI agents for news aggregation, technical trend analysis, live market data, AI-powered insights, and portfolio advice, collaborating to provide users with clear, actionable intelligence for smarter investing.

Designed for both novice and experienced investors, the app combines real-time news, technical indicators, and the latest AI models (including Gemini 2.5 Pro) in an intuitive dashboard. Users can analyze any stock ticker, explore AI-driven buy/hold/sell recommendations, and receive tailored portfolio suggestions based on their risk profile, all in one seamless experience.

Built with Python, Streamlit, and Google Cloud, this project demonstrates the power of collaborative AI agents and cloud-native deployment for next-generation financial analysis.

-Google ADK Hackathon (Jun-2025)

# Project Structure
/ai-stock-analyst  

├── agents/  

│ ├── news\_agent.py # News scraping/summarization  

│ ├── trends\_agent.py # Technical analysis  

│ ├── data\_agent.py # Real-time data fetching  

│ ├── insights\_agent.py # Investment advice generation  

│ └── portfolio\_agent.py # Risk-based recommendations  

├── orchestration/  

│ └── main\_adk.py # Agent coordination logic  

├── frontend/  

│ ├── app.py # Streamlit/Flask interface  

│ └── templates/ # HTML templates (if web UI)  

├── tests/ # Unit/integration tests  

├── infrastructure/  

│ ├── Dockerfile # Containerization  

│ └── cloudbuild.yaml # CI/CD pipeline  

├── docs/  

│ ├── ARCHITECTURE.md # System diagram explanation  

│ └── SETUP.md # Installation instructions  

└── requirements.txt # Python dependencies
