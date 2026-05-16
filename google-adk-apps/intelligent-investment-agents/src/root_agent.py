# src/root_agent.py - Complete Fixed Version
from google.adk.agents import Agent
from google.adk.tools import ToolContext
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def stock_screening_tool(query: str, tool_context: ToolContext = None) -> str:
    """Tool function for stock screening - let LLM present results"""
    try:
        # DON'T set skip_summarization - let LLM present the results
        from agents.stock_screener_final import stock_screening_function
        # Pass tool_context to the underlying function (but don't use skip_summarization)
        result = stock_screening_function(query)  # Pass None to avoid skip_summarization
        return result
    except Exception as e:
        return f"Error in stock screening: {str(e)}"

def style_theme_tool(query: str, tool_context: ToolContext = None) -> str:
    """Tool function for style and theme analysis - let LLM present results"""
    try:
        # DON'T set skip_summarization - let LLM present the results
        from agents.style_theme_agent import style_theme_analysis_function
        return style_theme_analysis_function(query)  # Pass None to avoid skip_summarization
    except Exception as e:
        return f"Error in style/theme analysis: {str(e)}"

def portfolio_risk_tool(query: str, tool_context: ToolContext = None) -> str:
    """Tool function for portfolio risk analysis - let LLM present results"""
    try:
        # DON'T set skip_summarization - let LLM present the results
        from agents.portfolio_risk_agent import portfolio_risk_analysis_function
        return portfolio_risk_analysis_function(query)  # Pass None to avoid skip_summarization
    except Exception as e:
        return f"Error in portfolio risk analysis: {str(e)}"

def multi_strategy_tool(query: str, tool_context: ToolContext = None) -> str:
    """Tool function for multi-strategy analysis - let LLM present results"""
    try:
        # DON'T set skip_summarization - let LLM present the results
        from agents.multi_strategy_agent import multi_strategy_analysis_function
        return multi_strategy_analysis_function(query)  # Pass None to avoid skip_summarization
    except Exception as e:
        return f"Error in multi-strategy analysis: {str(e)}"

class AdaptiveInvestmentPlatform(Agent):
    def __init__(self):
        super().__init__(
            name="adaptive_investment_platform",
            description="Adaptive Trading Intelligence System with 4 specialized agents",
            model="gemini-1.5-flash",
            tools=[stock_screening_tool, style_theme_tool, portfolio_risk_tool, multi_strategy_tool],
            instruction="""You are the Adaptive Trading Intelligence System.

CRITICAL: When you receive tool results, extract the formatted content from the result and display it directly to the user.

TOOL ROUTING RULES:
- Stock queries (find, show, search, screen, dividend, pe, price, nasdaq, tech, companies, filter, lowest, highest, value, stocks) → use stock_screening_tool
- Style queries (classify, style, growth, value, momentum, theme, ai, ev, fintech, healthcare, sector, analysis) → use style_theme_tool  
- Risk queries (risk, portfolio, stress, factor, concentration, attribution) → use portfolio_risk_tool
- Strategy queries (manager, overlap, correlation, multi, strategy) → use multi_strategy_tool

EXAMPLES:
- "Find tech stocks under $200" → stock_screening_tool
- "Classify healthcare stocks by investment style" → style_theme_tool
- "Show growth vs value stocks" → style_theme_tool
- "Analyze AI theme stocks" → style_theme_tool
- "Portfolio risk analysis" → portfolio_risk_tool

RESPONSE FORMAT:
1. Call the appropriate tool based on the query
2. Extract the formatted content from the tool result  
3. Display it directly to the user without modification
4. Do NOT add introductory text like "Here are the results" or "Based on the analysis"
5. Do NOT add disclaimers or additional commentary"""
        )
    def run(self, query: str) -> str:
        """Custom routing to ensure queries go to the right agents"""
        try:
            query_lower = query.lower()
            
            # Style and theme keywords - FORCE routing to style_theme_tool
            style_keywords = [
                'classify', 'style', 'growth', 'value', 'momentum', 'theme', 
                'ai', 'ev', 'fintech', 'healthcare', 'sector', 'analysis',
                'by investment style', 'by style', 'investment style'
            ]
            
            # Stock screening keywords
            stock_keywords = [
                'find', 'show', 'search', 'screen', 'dividend', 'pe', 'price', 
                'nasdaq', 'tech', 'companies', 'filter', 'lowest', 'highest', 
                'stocks', 'under', 'over', 'yield'
            ]
            
            # Risk keywords  
            risk_keywords = [
                'risk', 'portfolio', 'stress', 'factor', 'concentration', 
                'attribution', 'analyze risk'
            ]
            
            # Strategy keywords
            strategy_keywords = [
                'manager', 'overlap', 'correlation', 'multi', 'strategy'
            ]
            
            # Route based on keywords - Style queries get priority
            if any(keyword in query_lower for keyword in style_keywords):
                print(f"DEBUG: Routing to style_theme_tool for query: {query}")
                return style_theme_tool(query)
            elif any(keyword in query_lower for keyword in risk_keywords):
                print(f"DEBUG: Routing to portfolio_risk_tool for query: {query}")
                return portfolio_risk_tool(query)
            elif any(keyword in query_lower for keyword in strategy_keywords):
                print(f"DEBUG: Routing to multi_strategy_tool for query: {query}")
                return multi_strategy_tool(query)
            elif any(keyword in query_lower for keyword in stock_keywords):
                print(f"DEBUG: Routing to stock_screening_tool for query: {query}")
                return stock_screening_tool(query)
            else:
                # Default to stock screening
                print(f"DEBUG: Default routing to stock_screening_tool for query: {query}")
                return stock_screening_tool(query)
                
        except Exception as e:
            return f"Error: {str(e)}"

# Create the root agent instance
root_agent = AdaptiveInvestmentPlatform()
agent = root_agent
