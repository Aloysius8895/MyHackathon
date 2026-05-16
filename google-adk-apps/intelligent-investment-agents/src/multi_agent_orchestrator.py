# src/multi_agent_orchestrator.py
from google.adk.agents import Agent
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# Import all our agents
from agents.stock_screener_final import StockScreeningAgent
from agents.style_theme_agent import StyleThemeAgent
from agents.portfolio_risk_agent import PortfolioRiskAgent

def multi_agent_coordination_function(query: str) -> str:
    """
    Orchestrates multiple agents to provide comprehensive investment intelligence
    """
    try:
        orchestrator = InvestmentIntelligenceOrchestrator()
        return orchestrator.coordinate_agents(query)
    except Exception as e:
        return f"Error in multi-agent coordination: {str(e)}"

class InvestmentIntelligenceOrchestrator:
    """Orchestrates multiple investment intelligence agents"""
    
    def __init__(self):
        # Initialize all agents
        self.stock_screener = StockScreeningAgent()
        self.style_theme_agent = StyleThemeAgent()
        self.portfolio_risk_agent = PortfolioRiskAgent()
        
        # Define agent routing keywords
        self.agent_routing = {
            'stock_screener': ['find', 'screen', 'stocks', 'companies', 'search', 'filter', 'dividend', 'pe', 'price'],
            'style_theme': ['style', 'theme', 'growth', 'value', 'momentum', 'ai', 'ev', 'fintech', 'classify'],
            'portfolio_risk': ['risk', 'attribution', 'portfolio', 'stress', 'factor', 'concentration', 'scenario']
        }

    def coordinate_agents(self, query: str) -> str:
        """Main coordination logic"""
        try:
            query_lower = query.lower()
            
            # Determine which agents to engage
            agents_to_use = self.determine_agent_strategy(query_lower)
            
            if len(agents_to_use) == 1:
                return self.single_agent_response(agents_to_use[0], query)
            elif len(agents_to_use) > 1:
                return self.multi_agent_response(agents_to_use, query)
            else:
                return self.comprehensive_analysis(query)
                
        except Exception as e:
            return f"Error in agent coordination: {str(e)}"

    def determine_agent_strategy(self, query_lower: str) -> list:
        """Determine which agents should handle the query"""
        agents_needed = []
        
        # Check each agent's keywords
        for agent_name, keywords in self.agent_routing.items():
            if any(keyword in query_lower for keyword in keywords):
                agents_needed.append(agent_name)
        
        return agents_needed

    def single_agent_response(self, agent_name: str, query: str) -> str:
        """Handle query with single agent"""
        try:
            if agent_name == 'stock_screener':
                return self.stock_screener.run(query)
            elif agent_name == 'style_theme':
                return self.style_theme_agent.run(query)
            elif agent_name == 'portfolio_risk':
                return self.portfolio_risk_agent.run(query)
            else:
                return f"Unknown agent: {agent_name}"
                
        except Exception as e:
            return f"Error with {agent_name}: {str(e)}"

    def multi_agent_response(self, agents_to_use: list, query: str) -> str:
        """Handle query with multiple agents"""
        try:
            responses = {}
            
            # Get response from each relevant agent
            for agent_name in agents_to_use:
                try:
                    response = self.single_agent_response(agent_name, query)
                    responses[agent_name] = response
                except Exception as e:
                    responses[agent_name] = f"Error: {str(e)}"
            
            # Synthesize responses
            return self.synthesize_responses(responses, query)
            
        except Exception as e:
            return f"Error in multi-agent response: {str(e)}"

    def comprehensive_analysis(self, query: str) -> str:
        """Perform comprehensive analysis using all agents"""
        try:
            # Use all agents for comprehensive analysis
            stock_analysis = self.stock_screener.run(query)
            style_analysis = self.style_theme_agent.run(query)
            risk_analysis = self.portfolio_risk_agent.run(query)
            
            return f"""# 🎯 Comprehensive Investment Intelligence Analysis

## 📊 Stock Screening Results
{stock_analysis}

---

## 🎭 Style & Theme Analysis  
{style_analysis}

---

## ⚖️ Portfolio Risk Assessment
{risk_analysis}

---

## 💡 Integrated Investment Insights
This comprehensive analysis combines stock screening, style classification, and risk assessment to provide complete investment intelligence for institutional decision-making."""
            
        except Exception as e:
            return f"Error in comprehensive analysis: {str(e)}"

    def synthesize_responses(self, responses: dict, query: str) -> str:
        """Synthesize multiple agent responses into coherent analysis"""
        try:
            synthesis = f"# 🎯 Multi-Agent Investment Analysis\n"
            synthesis += f"**Query:** {query}\n\n"
            
            # Add each agent's response
            agent_titles = {
                'stock_screener': "📊 Stock Screening Results",
                'style_theme': "🎭 Style & Theme Classification", 
                'portfolio_risk': "⚖️ Portfolio Risk Analysis"
            }
            
            for agent_name, response in responses.items():
                if response and "Error:" not in response:
                    title = agent_titles.get(agent_name, f"{agent_name} Analysis")
                    synthesis += f"## {title}\n{response}\n\n---\n\n"
            
            # Add synthesis insights
            synthesis += "## 💡 Integrated Insights\n"
            synthesis += self.generate_synthesis_insights(responses, query)
            
            return synthesis
            
        except Exception as e:
            return f"Error synthesizing responses: {str(e)}"

    def generate_synthesis_insights(self, responses: dict, query: str) -> str:
        """Generate insights from combined agent responses"""
        insights = []
        
        # Analyze what agents were used
        if 'stock_screener' in responses and 'style_theme' in responses:
            insights.append("• **Investment Style Alignment**: Screening results classified by growth/value characteristics")
        
        if 'stock_screener' in responses and 'portfolio_risk' in responses:
            insights.append("• **Risk-Adjusted Selection**: Stock picks evaluated for portfolio risk impact")
        
        if 'style_theme' in responses and 'portfolio_risk' in responses:
            insights.append("• **Factor Risk Assessment**: Style exposures analyzed for portfolio construction")
        
        if len(responses) == 3:
            insights.append("• **Complete Investment Process**: Full pipeline from screening to risk management")
        
        # Add query-specific insights
        query_lower = query.lower()
        if 'tech' in query_lower:
            insights.append("• **Sector Focus**: Technology sector analysis with growth bias consideration")
        
        if 'dividend' in query_lower:
            insights.append("• **Income Strategy**: Dividend-focused screening with value style characteristics")
        
        return "\n".join(insights) if insights else "• **Multi-Agent Analysis**: Comprehensive investment intelligence delivered"

class MultiAgentOrchestrator(Agent):
    def __init__(self):
        super().__init__(
            name="investment_intelligence_orchestrator",
            description="Orchestrates multiple investment intelligence agents (Stock Screening, Style/Theme Classification, Portfolio Risk) to provide comprehensive investment analysis",
            model="gemini-1.5-flash", 
            tools=[multi_agent_coordination_function],
            instruction="""You are the master orchestrator for a sophisticated investment intelligence platform.

You coordinate multiple specialized agents:
1. Stock Screening Agent: Finds and filters stocks based on criteria
2. Style & Theme Classification Agent: Analyzes investment styles and themes
3. Portfolio Risk Attribution Agent: Performs risk analysis and attribution

Your job is to:
- Determine which agents are needed for each query
- Coordinate agent interactions
- Synthesize results into coherent investment intelligence
- Provide integrated insights that combine multiple agent perspectives

For any investment-related query, use the multi_agent_coordination_function to orchestrate the appropriate agents."""
        )

    def run(self, query: str) -> str:
        """Main orchestrator method"""
        return multi_agent_coordination_function(query)
