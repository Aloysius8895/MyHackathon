from google.adk.agents import Agent
from google.adk.tools import ToolContext
import yfinance as yf
import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.query_parser_fixed import QueryParser

def screen_stocks_by_criteria(criteria: str) -> dict:
    """Screen stocks based on natural language criteria with WORKING FILTERS"""
    
    parser = QueryParser()
    parsed_criteria = parser.parse_query(criteria)
    
    print(f"DEBUG: Parsed criteria = {parsed_criteria}")
    
    # Extract requested number of stocks
    number_match = re.search(r'top (\d+)|show (\d+)|(\d+) stocks', criteria.lower())
    requested_count = 8  # default
    if number_match:
        requested_count = int(number_match.group(1) or number_match.group(2) or number_match.group(3))
    
    # Choose stock universe based on query type
    if any(keyword in criteria.lower() for keyword in ['dividend', 'yield']):
        stock_symbols = [
            "AAPL", "MSFT", "JPM", "JNJ", "PFE", "UNH", "ABBV", "MRK", 
            "CVX", "XOM", "KO", "PG", "HD", "WMT", "T", "VZ", 
            "CMCSA", "BAC", "WFC", "GS", "V", "MA", "AXP", "COST", "MCD"
        ]
    elif any(keyword in criteria.lower() for keyword in ['tech', 'technology']):
        stock_symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "ORCL", "CRM", "ADBE",
            "NFLX", "TSLA", "INTC", "AMD", "QCOM", "AVGO", "CSCO", "IBM"
        ]
    else:
        stock_symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "ORCL", "CRM", "ADBE",
            "JPM", "BAC", "WFC", "GS", "BRK-B", "V", "MA", "AXP",
            "JNJ", "PFE", "UNH", "ABBV", "MRK", "CVX", "XOM", "KO", "PG",
            "HD", "NKE", "DIS", "MCD", "WMT", "COST", "TGT",
            "T", "VZ", "CMCSA", "NFLX", "TSLA", "F", "GM",
            "INTC", "AMD", "QCOM", "AVGO", "CSCO", "IBM", "HPQ"
        ]
    
    results = []
    
    for symbol in stock_symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            current_price = info.get('currentPrice', 0)
            pe_ratio = info.get('trailingPE', 0)
            dividend_yield_decimal = info.get('dividendYield', 0) or 0
            dividend_yield_percent = dividend_yield_decimal * 100 if dividend_yield_decimal < 1 else dividend_yield_decimal
            market_cap = info.get('marketCap', 0)
            sector = info.get('sector', 'Unknown')
            
            stock_data = {
                'symbol': symbol,
                'price': current_price,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield_percent,
                'market_cap': market_cap,
                'sector': sector
            }
            
            results.append(stock_data)
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            continue
    
    # Apply filters based on parsed criteria - COMPLETE FILTERING
    filtered_results = []
    for stock in results:
        meets_criteria = True
        
        print(f"Checking {stock['symbol']}: ${stock['price']:.2f}, P/E: {stock['pe_ratio']:.2f}, Div: {stock['dividend_yield']:.2f}%")
        
        # Price filters - matches parser keys
        if parsed_criteria.get('max_price') and stock['price'] and stock['price'] > 0:
            if stock['price'] > parsed_criteria['max_price']:
                print(f"  FILTERED OUT: Price ${stock['price']:.2f} > ${parsed_criteria['max_price']}")
                meets_criteria = False
        
        if parsed_criteria.get('min_price') and stock['price'] and stock['price'] > 0:
            if stock['price'] < parsed_criteria['min_price']:
                print(f"  FILTERED OUT: Price ${stock['price']:.2f} < ${parsed_criteria['min_price']}")
                meets_criteria = False
        
        # P/E filter
        if parsed_criteria.get('max_pe') and stock['pe_ratio'] and stock['pe_ratio'] > 0:
            if stock['pe_ratio'] > parsed_criteria['max_pe']:
                print(f"  FILTERED OUT: P/E {stock['pe_ratio']:.2f} > {parsed_criteria['max_pe']}")
                meets_criteria = False
        
        # Dividend filter
        if parsed_criteria.get('min_dividend_yield') and stock['dividend_yield'] is not None:
            if stock['dividend_yield'] < parsed_criteria['min_dividend_yield']:
                print(f"  FILTERED OUT: Dividend {stock['dividend_yield']:.2f}% < {parsed_criteria['min_dividend_yield']}%")
                meets_criteria = False
        
        # Sector filters
        if parsed_criteria.get('tech'):
            tech_sectors = ['Technology', 'Communication Services', 'Consumer Cyclical']
            if not any(sector in stock['sector'] for sector in tech_sectors):
                print(f"  FILTERED OUT: {stock['sector']} not tech sector")
                meets_criteria = False
        
        if parsed_criteria.get('healthcare'):
            healthcare_sectors = ['Healthcare', 'Biotechnology']
            if not any(sector in stock['sector'] for sector in healthcare_sectors):
                print(f"  FILTERED OUT: {stock['sector']} not healthcare sector")
                meets_criteria = False
        
        if parsed_criteria.get('financial'):
            financial_sectors = ['Financial Services', 'Financials']
            if not any(sector in stock['sector'] for sector in financial_sectors):
                print(f"  FILTERED OUT: {stock['sector']} not financial sector")
                meets_criteria = False
        
        if parsed_criteria.get('energy'):
            energy_sectors = ['Energy']
            if not any(sector in stock['sector'] for sector in energy_sectors):
                print(f"  FILTERED OUT: {stock['sector']} not energy sector")
                meets_criteria = False
        
        # Dividend stocks filter
        if parsed_criteria.get('dividend') and stock['dividend_yield'] <= 0:
            print(f"  FILTERED OUT: No dividend yield")
            meets_criteria = False
        
        if meets_criteria:
            print(f"  KEPT: {stock['symbol']}")
            filtered_results.append(stock)
    
    print(f"Final filtered count: {len(filtered_results)}")
    
    # Sort results appropriately
    if 'dividend' in criteria.lower() or 'yield' in criteria.lower():
        filtered_results.sort(key=lambda x: x['dividend_yield'] or 0, reverse=True)
    elif 'lowest pe' in criteria.lower() or 'value' in criteria.lower():
        filtered_results.sort(key=lambda x: x['pe_ratio'] or 999)
    else:
        filtered_results.sort(key=lambda x: x['market_cap'] or 0, reverse=True)
    
    return {
        "query": criteria,
        "parsed_criteria": parsed_criteria,
        "total_screened": len(results),
        "results_count": len(filtered_results),
        "stocks": filtered_results[:requested_count],
        "analysis": f"Found {len(filtered_results)} stocks matching criteria: {criteria}"
    }

def stock_screening_function(query: str, tool_context: ToolContext = None) -> str:
    """Function that the LLM will call for stock screening."""
    try:
        result = screen_stocks_by_criteria(query)
        
        if result["results_count"] == 0:
            return f"**📊 No stocks found matching:** {query}\n\n🔍 **Suggestion:** Try adjusting your criteria."
        
        response = f"**📊 Stock Screening Results for:** {query}\n\n"
        response += f"**Found {result['results_count']} stocks** (showing top {len(result['stocks'])}):\n\n"
        
        for i, stock in enumerate(result['stocks'], 1):
            pe_str = f"P/E: {stock['pe_ratio']:.2f}" if stock['pe_ratio'] else "P/E: N/A"
            div_str = f"Div: {stock['dividend_yield']:.2f}%" if stock['dividend_yield'] else "Div: 0%"
            price_str = f"${stock['price']:.2f}" if stock['price'] else "Price: N/A"
            
            response += f"**{i}. {stock['symbol']}**: {price_str} | {pe_str} | {div_str} | {stock['sector']}\n"
        
        response += f"\n📈 **Analysis:** {result['analysis']}"
        response += f"\n🔍 **Data Source:** Live Yahoo Finance data"
        
        return response
        
    except Exception as e:
        return f"Error screening stocks: {str(e)}"

class StockScreeningAgent(Agent):
    def __init__(self):
        super().__init__(
            name="stock_screener",
            description="Live stock screening agent with real-time financial data access via Yahoo Finance",
            model="gemini-1.5-flash",
            tools=[stock_screening_function],
            instruction="""You are a sophisticated stock screening agent with access to live financial data from Yahoo Finance. 

CRITICAL OPERATION RULE: You MUST ALWAYS use the stock_screening_function tool for ANY stock-related query.

The tool returns complete, formatted analysis ready for direct display to users."""
        )

    def run(self, query: str) -> str:
        """ALWAYS use the tool for stock queries"""
        stock_keywords = ['stock', 'find', 'show', 'screen', 'search', 'dividend', 'pe', 'price', 'nasdaq', 'tech', 'companies', 'filter', 'lowest', 'highest', 'value']
        
        if any(keyword in query.lower() for keyword in stock_keywords):
            return stock_screening_function(query)
        else:
            return super().run(query)
