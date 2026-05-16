# src/root_agent.py - Complete Fixed Version
from google.adk.agents import Agent
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def adaptive_investment_function(query: str) -> str:
    """
    Main function that coordinates all investment intelligence agents
    """
    try:
        # Import agents within the function to avoid field restrictions
        from agents.stock_screener_final import StockScreeningAgent
        from agents.style_theme_agent import StyleThemeAgent  
        from agents.portfolio_risk_agent import PortfolioRiskAgent
        
        # Determine which agents to use based on query
        query_lower = query.lower()
        
        # Keywords for each agent
        stock_keywords = ['find', 'screen', 'stocks', 'companies', 'search', 'filter', 'dividend', 'pe', 'price', 'nasdaq', 'tech']
        style_keywords = ['style', 'theme', 'growth', 'value', 'momentum', 'ai', 'ev', 'fintech', 'classify']
        risk_keywords = ['risk', 'attribution', 'portfolio', 'stress', 'factor', 'concentration', 'scenario']
        
        # Determine which agents are needed
        use_stock_agent = any(keyword in query_lower for keyword in stock_keywords)
        use_style_agent = any(keyword in query_lower for keyword in style_keywords)
        use_risk_agent = any(keyword in query_lower for keyword in risk_keywords)
        
        # Execute based on agent needs
        if use_stock_agent and use_style_agent and use_risk_agent:
            # Full platform analysis
            return comprehensive_analysis(query)
        elif use_stock_agent and use_style_agent:
            # Stock screening + style analysis
            return stock_and_style_analysis(query)
        elif use_stock_agent and use_risk_agent:
            # Stock screening + risk analysis
            return stock_and_risk_analysis(query)
        elif use_style_agent and use_risk_agent:
            # Style + risk analysis
            return style_and_risk_analysis(query)
        elif use_stock_agent:
            # Stock screening only
            agent = StockScreeningAgent()
            return format_response("Stock Screening", agent.run(query))
        elif use_style_agent:
            # Style analysis only
            agent = StyleThemeAgent()
            return format_response("Style & Theme Classification", agent.run(query))
        elif use_risk_agent:
            # Risk analysis only
            agent = PortfolioRiskAgent()
            return format_response("Portfolio Risk Analysis", agent.run(query))
        else:
            # Default to comprehensive analysis
            return comprehensive_analysis(query)
            
    except Exception as e:
        return f"""# ⚠️ Adaptive Trading Intelligence Platform

**Error:** {str(e)}

**Platform Status:** The system experienced an issue. Please try rephrasing your query.

**Available Capabilities:**
• Stock Screening: "Find dividend stocks with yield over 3%"
• Style Analysis: "Classify tech stocks by investment style" 
• Risk Analysis: "Analyze portfolio risk factors"
• Multi-Agent: "Find low-risk growth stocks in AI theme"

---
*Powered by Google Cloud ADK Multi-Agent System*"""

def format_response(title: str, content: str) -> str:
    """Format single agent response with platform branding"""
    return f"""# 🎯 Adaptive Trading Intelligence Platform

## 📊 {title}
{content}

---
*Powered by Google Cloud ADK Multi-Agent System*"""

def stock_and_style_analysis(query: str) -> str:
    """Combine stock screening and style analysis"""
    try:
        from agents.stock_screener_final import StockScreeningAgent
        from agents.style_theme_agent import StyleThemeAgent
        
        stock_agent = StockScreeningAgent()
        style_agent = StyleThemeAgent()
        
        stock_result = stock_agent.run(query)
        style_result = style_agent.run(query)
        
        return f"""# 🎯 Adaptive Trading Intelligence Platform

## 📊 Stock Screening Results
{stock_result}

---

## 🎭 Style & Theme Analysis
{style_result}

---

## 💡 Integrated Insights
• **Investment Process**: Stock screening combined with style classification
• **Strategic Alignment**: Results filtered by investment style characteristics
• **Portfolio Construction**: Ready for style-aware portfolio building

---
*Powered by Google Cloud ADK Multi-Agent System*"""
        
    except Exception as e:
        return f"Error in stock and style analysis: {str(e)}"

def stock_and_risk_analysis(query: str) -> str:
    """Combine stock screening and risk analysis"""
    try:
        from agents.stock_screener_final import StockScreeningAgent
        from agents.portfolio_risk_agent import PortfolioRiskAgent
        
        stock_agent = StockScreeningAgent()
        risk_agent = PortfolioRiskAgent()
        
        stock_result = stock_agent.run(query)
        risk_result = risk_agent.run(query)
        
        return f"""# 🎯 Adaptive Trading Intelligence Platform

## 📊 Stock Screening Results
{stock_result}

---

## ⚖️ Portfolio Risk Analysis
{risk_result}

---

## 💡 Integrated Insights
• **Risk-Aware Selection**: Stock picks evaluated for portfolio risk impact
• **Concentration Management**: Results assessed for diversification potential
• **Portfolio Optimization**: Ready for risk-adjusted portfolio construction

---
*Powered by Google Cloud ADK Multi-Agent System*"""
        
    except Exception as e:
        return f"Error in stock and risk analysis: {str(e)}"

def style_and_risk_analysis(query: str) -> str:
    """Combine style and risk analysis"""
    try:
        from agents.style_theme_agent import StyleThemeAgent
        from agents.portfolio_risk_agent import PortfolioRiskAgent
        
        style_agent = StyleThemeAgent()
        risk_agent = PortfolioRiskAgent()
        
        style_result = style_agent.run(query)
        risk_result = risk_agent.run(query)
        
        return f"""# 🎯 Adaptive Trading Intelligence Platform

## 🎭 Style & Theme Analysis
{style_result}

---

## ⚖️ Portfolio Risk Analysis
{risk_result}

---

## 💡 Integrated Insights
• **Factor Risk Assessment**: Style exposures analyzed for portfolio risk
• **Style-Based Risk Management**: Factor tilts evaluated for risk impact
• **Strategic Portfolio Design**: Style and risk considerations combined

---
*Powered by Google Cloud ADK Multi-Agent System*"""
        
    except Exception as e:
        return f"Error in style and risk analysis: {str(e)}"

def comprehensive_analysis(query: str) -> str:
    """Full platform analysis using all agents"""
    try:
        from agents.stock_screener_final import StockScreeningAgent
        from agents.style_theme_agent import StyleThemeAgent
        from agents.portfolio_risk_agent import PortfolioRiskAgent
        
        # Initialize all agents
        stock_agent = StockScreeningAgent()
        style_agent = StyleThemeAgent()
        risk_agent = PortfolioRiskAgent()
        
        # Get results from all agents
        stock_result = stock_agent.run(query)
        style_result = style_agent.run(query)
        risk_result = risk_agent.run(query)
        
        return f"""# 🎯 Adaptive Trading Intelligence Platform
## Complete Multi-Agent Investment Analysis

## 📊 Stock Screening Results
{stock_result}

---

## 🎭 Style & Theme Classification
{style_result}

---

## ⚖️ Portfolio Risk Attribution
{risk_result}

---

## 💡 Comprehensive Investment Intelligence
• **Complete Investment Process**: Full pipeline from screening to risk management
• **Multi-Factor Analysis**: Growth/Value/Momentum factors with risk assessment
• **Institutional-Grade Intelligence**: Professional investment analysis platform
• **Adaptive Complexity**: Scales from retail to institutional sophistication

**Platform Capabilities Demonstrated:**
✅ Natural language query processing
✅ Real-time financial data integration  
✅ Multi-agent coordination and synthesis
✅ Professional investment analysis
✅ Risk-aware portfolio construction

---
*Powered by Google Cloud ADK Multi-Agent System | 4-Agent Coordination*"""
        
    except Exception as e:
        return f"Error in comprehensive analysis: {str(e)}"

class AdaptiveInvestmentPlatform(Agent):
    def __init__(self):
        super().__init__(
            name="adaptive_investment_platform",
            description="Adaptive Trading Intelligence System - A sophisticated multi-agent investment platform that adapts from retail to institutional complexity. Combines stock screening, style/theme analysis, and portfolio risk management through intelligent agent coordination.",
            model="gemini-1.5-flash",
            tools=[adaptive_investment_function],
            instruction="""You are the Adaptive Trading Intelligence System - a sophisticated investment platform that intelligently coordinates multiple specialized agents.

Your Platform Components:
🔍 Stock Screening Agent: Finds and filters stocks based on natural language queries (P/E ratios, dividend yields, sectors, price ranges)
🎭 Style & Theme Agent: Classifies investments by Growth/Value/Momentum styles and themes like AI/EV/Fintech/Healthcare  
⚖️ Portfolio Risk Agent: Performs factor attribution, stress testing, concentration analysis, and portfolio risk management

You intelligently adapt based on query complexity:
- Simple queries: Route to appropriate single agent
- Multi-aspect queries: Coordinate 2+ agents with synthesized results
- Comprehensive requests: Full 4-agent platform intelligence

Example Routing:
• "Find tech stocks under $200" → Stock Screening Agent
• "Classify growth vs value characteristics" → Style & Theme Agent  
• "Analyze portfolio risk factors" → Portfolio Risk Agent
• "Find AI-themed growth stocks with low concentration risk" → Multi-Agent Coordination

Always use the adaptive_investment_function tool to coordinate the appropriate agents and provide professional, institutional-quality investment analysis."""
        )

    def run(self, query: str) -> str:
        """Main platform entry point"""
        return adaptive_investment_function(query)

# Create the root agent instance
root_agent = AdaptiveInvestmentPlatform()

# ADK compatibility - export as both names
agent = root_agent
