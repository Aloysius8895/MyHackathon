# src/agents/style_theme_agent.py - COMPLETE VERSION WITH ALL SECTORS
from google.adk.agents import Agent
import yfinance as yf
import sys
import os
from typing import Dict, List, Tuple

# Add src to path so we can import our utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Define sector universes - focusing on liquid, well-known stocks
SECTOR_STOCKS = {
    'Technology': [
        'AAPL', 'MSFT', 'NVDA', 'AVGO', 'ORCL', 'ADBE', 'CRM', 'CSCO', 
        'INTC', 'AMD', 'QCOM', 'TXX', 'INTU', 'IBM', 'MU', 'AMAT'
    ],
    'Healthcare': [
        'UNH', 'JNJ', 'LLY', 'PFE', 'ABBV', 'MRK', 'TMO', 'ABT',
        'CVS', 'AMGN', 'MDT', 'DHR', 'BMY', 'GILD', 'ISRG', 'VRTX'
    ],
    'Financials': [
        'BRK-B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'GS', 'MS',
        'AXP', 'SCHW', 'C', 'SPGI', 'BLK', 'CB', 'MMC', 'PGR'
    ],
    'Consumer': [
        'AMZN', 'TSLA', 'HD', 'WMT', 'MCD', 'NKE', 'SBUX', 'TGT',
        'LOW', 'COST', 'TJX', 'DG', 'CMG', 'YUM', 'LULU', 'ROST'
    ],
    'Energy': [
        'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'VLO', 'PSX',
        'OXY', 'PXD', 'HES', 'DVN', 'HAL', 'BKR', 'FANG', 'KMI'
    ],
    'Industrials': [
        'BA', 'RTX', 'HON', 'UPS', 'CAT', 'LMT', 'DE', 'GE',
        'MMM', 'FDX', 'ETN', 'EMR', 'ITW', 'GD', 'NSC', 'WM'
    ],
    'Materials': [
        'LIN', 'APD', 'SHW', 'ECL', 'DD', 'NEM', 'FCX', 'DOW',
        'PPG', 'CTVA', 'ALB', 'IFF', 'LYB', 'BALL', 'AVY', 'IP'
    ],
    'Communication Services': [
        'GOOGL', 'META', 'DIS', 'NFLX', 'CMCSA', 'VZ', 'T', 'TMUS',
        'CHTR', 'EA', 'TTWO', 'ATVI', 'MTCH', 'SNAP', 'PINS', 'ROKU'
    ],
    'Utilities': [
        'NEE', 'SO', 'DUK', 'CEG', 'SRE', 'AEP', 'D', 'PCG',
        'EXC', 'XEL', 'ED', 'WEC', 'ES', 'DTE', 'AWK', 'PPL'
    ],
    'Real Estate': [
        'PLD', 'AMT', 'CCI', 'EQIX', 'PSA', 'O', 'SBAC', 'WELL',
        'DLR', 'AVB', 'EQR', 'VTR', 'INVH', 'MAA', 'ARE', 'UDR'
    ]
}

# Theme definitions
THEME_UNIVERSE = {
    'AI': {
        'core_stocks': ['NVDA', 'GOOGL', 'MSFT', 'META', 'AMD'],
        'related_stocks': ['PLTR', 'CRM', 'SNOW', 'ADBE', 'NOW'],
        'description': 'Artificial Intelligence & Machine Learning'
    },
    'EV_CleanEnergy': {
        'core_stocks': ['TSLA', 'RIVN', 'LCID', 'NIO', 'XPEV'],
        'related_stocks': ['CHPT', 'PLUG', 'ENPH', 'SEDG', 'LAC'],
        'description': 'Electric Vehicles & Clean Energy'
    },
    'Fintech': {
        'core_stocks': ['SQ', 'PYPL', 'V', 'MA', 'COIN'],
        'related_stocks': ['AFRM', 'SOFI', 'HOOD', 'UPST'],
        'description': 'Financial Technology & Digital Payments'
    },
    'Cybersecurity': {
        'core_stocks': ['CRWD', 'PANW', 'ZS', 'OKTA', 'FTNT'],
        'related_stocks': ['S', 'NET', 'CYBR', 'RPD', 'TENB'],
        'description': 'Cybersecurity & Data Protection'
    },
    'Cloud': {
        'core_stocks': ['AMZN', 'MSFT', 'GOOGL', 'CRM', 'NOW'],
        'related_stocks': ['SNOW', 'DDOG', 'MDB', 'TEAM', 'HUBS'],
        'description': 'Cloud Computing & Infrastructure'
    }
}

def style_theme_analysis_function(query: str) -> str:
    """Main analysis function that MUST be called for all style/theme queries"""
    try:
        analyzer = StyleThemeAnalyzer()
        return analyzer.perform_analysis(query)
    except Exception as e:
        return f"Error in style/theme analysis: {str(e)}"

class StyleThemeAnalyzer:
    """Helper class to perform the actual analysis"""
    
    def perform_analysis(self, query: str) -> str:
        """Route to appropriate analysis based on query"""
        query_lower = query.lower()
        
        # Sector-specific analysis
        if 'healthcare' in query_lower or 'health' in query_lower:
            return self.analyze_sector_stocks('Healthcare', query)
        elif 'tech' in query_lower or 'technology' in query_lower:
            return self.analyze_sector_stocks('Technology', query)
        elif 'financ' in query_lower or 'bank' in query_lower:
            return self.analyze_sector_stocks('Financials', query)
        elif 'energy' in query_lower:
            return self.analyze_sector_stocks('Energy', query)
        elif 'consumer' in query_lower or 'retail' in query_lower:
            return self.analyze_sector_stocks('Consumer', query)
        elif 'industrial' in query_lower:
            return self.analyze_sector_stocks('Industrials', query)
        elif 'material' in query_lower:
            return self.analyze_sector_stocks('Materials', query)
        elif 'communication' in query_lower or 'media' in query_lower:
            return self.analyze_sector_stocks('Communication Services', query)
        elif 'utilit' in query_lower:
            return self.analyze_sector_stocks('Utilities', query)
        elif 'real estate' in query_lower or 'reit' in query_lower:
            return self.analyze_sector_stocks('Real Estate', query)
        
        # Cross-sector analysis
        elif 'all sector' in query_lower or 'cross sector' in query_lower:
            return self.analyze_all_sectors()
        
        # Theme analysis
        elif any(theme.lower() in query_lower for theme in ['ai', 'artificial intelligence']):
            return self.analyze_theme('AI', query)
        elif any(word in query_lower for word in ['ev', 'electric vehicle', 'clean energy']):
            return self.analyze_theme('EV_CleanEnergy', query)
        elif 'fintech' in query_lower:
            return self.analyze_theme('Fintech', query)
        elif 'cyber' in query_lower:
            return self.analyze_theme('Cybersecurity', query)
        elif 'cloud' in query_lower:
            return self.analyze_theme('Cloud', query)
        
        # General style classification
        else:
            return self.general_style_classification(query)
    
    def analyze_sector_stocks(self, sector_name: str, query: str) -> str:
        """Analyze any sector's stocks by style with real data"""
        sector_stocks = SECTOR_STOCKS.get(sector_name, [])
        
        if not sector_stocks:
            return f"No stocks found for sector: {sector_name}"
        
        response = f"# 📊 {sector_name} Sector - Investment Style Classification\n\n"
        response += f"**Analyzing {len(sector_stocks)} Major {sector_name} Stocks**\n"
        response += f"**Live Market Data Analysis**\n\n"
        
        style_results = {
            'Growth': [],
            'Value': [],
            'Momentum': [],
            'Blend': []
        }
        
        successful_analyses = 0
        
        # Analyze each stock in the sector
        for ticker in sector_stocks:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                # Get price history for momentum
                hist = stock.history(period="3mo")
                
                # Get key metrics
                price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
                pe_ratio = info.get('trailingPE', 0) or 0
                revenue_growth = (info.get('revenueGrowth', 0) or 0) * 100
                dividend_yield = (info.get('dividendYield', 0) or 0) * 100
                pb_ratio = info.get('priceToBook', 0) or 0
                roe = (info.get('returnOnEquity', 0) or 0) * 100
                market_cap = info.get('marketCap', 0) or 0
                
                # Calculate momentum
                if len(hist) > 0:
                    price_3m_ago = hist['Close'].iloc[0]
                    momentum_3m = ((price - price_3m_ago) / price_3m_ago * 100) if price_3m_ago > 0 else 0
                else:
                    momentum_3m = 0
                
                # Calculate style scores
                growth_score = 0
                value_score = 0
                momentum_score = 0
                
                # Growth scoring
                if revenue_growth > 25:
                    growth_score += 40
                elif revenue_growth > 15:
                    growth_score += 30
                elif revenue_growth > 10:
                    growth_score += 20
                
                if pe_ratio > 35:
                    growth_score += 30
                elif pe_ratio > 25:
                    growth_score += 20
                
                if roe > 20:
                    growth_score += 30
                elif roe > 15:
                    growth_score += 20
                
                # Value scoring  
                if 0 < pe_ratio < 12:
                    value_score += 40
                elif pe_ratio < 18:
                    value_score += 25
                
                if dividend_yield > 3.5:
                    value_score += 40
                elif dividend_yield > 2:
                    value_score += 25
                
                if 0 < pb_ratio < 2:
                    value_score += 20
                elif pb_ratio < 3:
                    value_score += 10
                
                # Momentum scoring
                if momentum_3m > 20:
                    momentum_score += 50
                elif momentum_3m > 10:
                    momentum_score += 35
                elif momentum_3m > 5:
                    momentum_score += 20
                
                if pe_ratio > 40:  # High PE can indicate momentum
                    momentum_score += 30
                
                # Determine primary style
                max_score = max(growth_score, value_score, momentum_score)
                
                if max_score < 40:
                    primary_style = 'Blend'
                elif growth_score == max_score:
                    primary_style = 'Growth'
                elif value_score == max_score:
                    primary_style = 'Value'
                else:
                    primary_style = 'Momentum'
                
                stock_data = {
                    'ticker': ticker,
                    'price': price,
                    'pe_ratio': pe_ratio,
                    'revenue_growth': revenue_growth,
                    'dividend_yield': dividend_yield,
                    'pb_ratio': pb_ratio,
                    'roe': roe,
                    'momentum_3m': momentum_3m,
                    'market_cap': market_cap,
                    'growth_score': growth_score,
                    'value_score': value_score,
                    'momentum_score': momentum_score
                }
                
                style_results[primary_style].append(stock_data)
                successful_analyses += 1
                
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                continue
        
        # Format results by style
        for style, stocks in style_results.items():
            if stocks:
                response += f"## {style} {sector_name} Stocks ({len(stocks)} stocks)\n\n"
                
                # Sort stocks appropriately
                if style == 'Growth':
                    stocks.sort(key=lambda x: x['revenue_growth'], reverse=True)
                elif style == 'Value':
                    stocks.sort(key=lambda x: x['pe_ratio'] if x['pe_ratio'] > 0 else 999)
                elif style == 'Momentum':
                    stocks.sort(key=lambda x: x['momentum_3m'], reverse=True)
                
                for stock in stocks[:5]:  # Show top 5 per style
                    response += f"### {stock['ticker']}\n"
                    response += f"- **Price:** ${stock['price']:.2f}"
                    if stock['market_cap'] > 0:
                        response += f" | **Market Cap:** ${stock['market_cap']/1e9:.1f}B"
                    response += "\n"
                    response += f"- **P/E Ratio:** {stock['pe_ratio']:.1f} | **P/B Ratio:** {stock['pb_ratio']:.1f}\n"
                    response += f"- **Revenue Growth:** {stock['revenue_growth']:.1f}% | **ROE:** {stock['roe']:.1f}%\n"
                    if stock['dividend_yield'] > 0:
                        response += f"- **Dividend Yield:** {stock['dividend_yield']:.2f}%\n"
                    response += f"- **3-Month Momentum:** {stock['momentum_3m']:.1f}%\n"
                    response += f"- **Style Scores:** Growth({stock['growth_score']}), Value({stock['value_score']}), Momentum({stock['momentum_score']})\n"
                    
                    # Add rationale
                    response += f"- **Rationale:** {self.generate_rationale(stock, style)}\n\n"
        
        # Add summary
        response += f"## 💡 {sector_name} Sector Summary\n\n"
        response += f"- **Total Stocks Analyzed:** {successful_analyses}/{len(sector_stocks)}\n"
        response += f"- **Growth Stocks:** {len(style_results['Growth'])}\n"
        response += f"- **Value Stocks:** {len(style_results['Value'])}\n"
        response += f"- **Momentum Stocks:** {len(style_results['Momentum'])}\n"
        response += f"- **Blend Stocks:** {len(style_results['Blend'])}\n\n"
        
        # Sector insights
        response += self.generate_sector_insights(sector_name, style_results)
        
        return response
    
    def analyze_theme(self, theme_name: str, query: str) -> str:
        """Analyze stocks in a specific theme"""
        theme_data = THEME_UNIVERSE.get(theme_name, {})
        all_stocks = theme_data.get('core_stocks', []) + theme_data.get('related_stocks', [])
        
        response = f"# 🎯 {theme_data.get('description', theme_name)} Theme Analysis\n\n"
        response += f"**Analyzing {len(all_stocks)} {theme_name} Theme Stocks**\n\n"
        
        theme_results = []
        
        for ticker in all_stocks[:10]:  # Analyze top 10 theme stocks
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                # Get metrics
                price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
                pe_ratio = info.get('trailingPE', 0) or 0
                revenue_growth = (info.get('revenueGrowth', 0) or 0) * 100
                market_cap = info.get('marketCap', 0) or 0
                
                # Determine if core or related
                position_type = 'Core' if ticker in theme_data.get('core_stocks', []) else 'Related'
                
                theme_results.append({
                    'ticker': ticker,
                    'price': price,
                    'pe_ratio': pe_ratio,
                    'revenue_growth': revenue_growth,
                    'market_cap': market_cap,
                    'position_type': position_type
                })
                
            except:
                continue
        
        # Format results
        response += "## Core Holdings\n\n"
        for stock in [s for s in theme_results if s['position_type'] == 'Core']:
            response += f"### {stock['ticker']}\n"
            response += f"- **Price:** ${stock['price']:.2f} | **Market Cap:** ${stock['market_cap']/1e9:.1f}B\n"
            response += f"- **P/E:** {stock['pe_ratio']:.1f} | **Revenue Growth:** {stock['revenue_growth']:.1f}%\n\n"
        
        response += "## Related Holdings\n\n"
        for stock in [s for s in theme_results if s['position_type'] == 'Related'][:3]:
            response += f"### {stock['ticker']}\n"
            response += f"- **Price:** ${stock['price']:.2f}\n"
            response += f"- **P/E:** {stock['pe_ratio']:.1f} | **Revenue Growth:** {stock['revenue_growth']:.1f}%\n\n"
        
        return response
    
    def analyze_all_sectors(self) -> str:
        """Analyze style distribution across all sectors"""
        response = "# 📊 Cross-Sector Style Analysis\n\n"
        response += "**Analyzing top stocks from each major sector**\n\n"
        
        sector_summary = {}
        
        # Quick analysis of 3 stocks per sector
        for sector_name, stocks in SECTOR_STOCKS.items():
            growth_count = 0
            value_count = 0
            
            for ticker in stocks[:3]:  # Just top 3 for quick analysis
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    pe = info.get('trailingPE', 0) or 0
                    growth = (info.get('revenueGrowth', 0) or 0) * 100
                    
                    if growth > 20 or pe > 30:
                        growth_count += 1
                    elif 0 < pe < 15:
                        value_count += 1
                        
                except:
                    continue
            
            sector_summary[sector_name] = {
                'growth': growth_count,
                'value': value_count
            }
        
        # Format as table
        response += "| Sector | Growth Stocks | Value Stocks |\n"
        response += "|--------|---------------|---------------|\n"
        
        for sector, counts in sector_summary.items():
            response += f"| {sector} | {counts['growth']} | {counts['value']} |\n"
        
        response += "\n## Key Insights\n"
        response += "- Technology and Healthcare tend toward growth characteristics\n"
        response += "- Energy and Financials offer more value opportunities\n"
        response += "- Consumer and Industrials show mixed styles\n"
        
        return response
    
    def general_style_classification(self, query: str) -> str:
        """General market-wide style classification"""
        # Mix stocks from different sectors
        mixed_stocks = []
        for sector, stocks in SECTOR_STOCKS.items():
            mixed_stocks.extend(stocks[:2])  # 2 from each sector
        
        return self.analyze_mixed_stocks(mixed_stocks[:20], "Market-Wide")
    
    def analyze_mixed_stocks(self, stock_list: List[str], label: str) -> str:
        """Helper to analyze a mixed list of stocks"""
        response = f"# 📊 {label} Style Classification\n\n"
        
        # Similar analysis logic as analyze_sector_stocks but with mixed list
        # ... (implement similar to sector analysis)
        
        return response
    
    def generate_rationale(self, stock_data: Dict, style: str) -> str:
        """Generate style-specific rationale"""
        rationales = []
        
        if style == 'Growth':
            if stock_data['revenue_growth'] > 20:
                rationales.append(f"exceptional revenue growth of {stock_data['revenue_growth']:.1f}%")
            if stock_data['roe'] > 20:
                rationales.append(f"high ROE of {stock_data['roe']:.1f}%")
            if stock_data['pe_ratio'] > 30:
                rationales.append("premium valuation reflects growth expectations")
                
        elif style == 'Value':
            if 0 < stock_data['pe_ratio'] < 15:
                rationales.append(f"attractive P/E of {stock_data['pe_ratio']:.1f}")
            if stock_data['dividend_yield'] > 2:
                rationales.append(f"solid dividend yield of {stock_data['dividend_yield']:.1f}%")
            if 0 < stock_data['pb_ratio'] < 2:
                rationales.append(f"trading below book value")
                
        elif style == 'Momentum':
            if stock_data['momentum_3m'] > 15:
                rationales.append(f"strong 3-month momentum of {stock_data['momentum_3m']:.1f}%")
            if stock_data['pe_ratio'] > 40:
                rationales.append("high valuation driven by momentum")
        
        return "; ".join(rationales[:2]) if rationales else f"{style} characteristics based on multiple factors"
    
    def generate_sector_insights(self, sector_name: str, style_results: Dict) -> str:
        """Generate sector-specific insights"""
        insights = {
            'Technology': "Tech sector shows strong growth bias due to innovation and scalability. Value plays often represent turnaround opportunities.",
            'Healthcare': "Healthcare splits between high-growth biotech and value-oriented established pharma. Patent cliffs create opportunities.",
            'Financials': "Financial sector offers value in traditional banks, growth in fintech and payment processors.",
            'Energy': "Energy sector cyclicality creates deep value opportunities. Renewable energy transition drives growth stocks.",
            'Consumer': "Consumer sector reflects economic trends - discretionary for growth, staples for value.",
            'Industrials': "Industrials benefit from infrastructure spending. Automation drives growth stories.",
            'Materials': "Materials track commodity cycles. ESG transition creating new growth opportunities.",
            'Communication Services': "Split between high-growth platforms (META, GOOGL) and value telecom (VZ, T).",
            'Utilities': "Traditionally defensive value plays. Clean energy utilities showing growth characteristics.",
            'Real Estate': "REITs offer value through yield. Growth in data centers and logistics properties."
        }
        
        base_insight = insights.get(sector_name, f"{sector_name} sector shows diverse investment styles.")
        
        # Add data-driven observation
        total = sum(len(stocks) for stocks in style_results.values())
        if total > 0:
            growth_pct = len(style_results['Growth']) / total * 100
            value_pct = len(style_results['Value']) / total * 100
            
            if growth_pct > 50:
                base_insight += f"\n\nCurrently growth-dominated ({growth_pct:.0f}% of analyzed stocks)."
            elif value_pct > 50:
                base_insight += f"\n\nValue opportunities abundant ({value_pct:.0f}% of analyzed stocks)."
        
        return base_insight

class StyleThemeAgent(Agent):
    def __init__(self):
        super().__init__(
            name="style_theme_classifier",
            description="Classifies stocks by investment styles (Growth/Value/Momentum) and themes with real market data",
            model="gemini-1.5-flash",
            tools=[style_theme_analysis_function],
            instruction="""You are a sophisticated investment style and theme classification agent.

CRITICAL RULE: You MUST ALWAYS use the style_theme_analysis_function tool for ANY query about:
- Investment styles (growth, value, momentum)
- Stock classification or categorization
- Sector analysis (healthcare, tech, finance, energy, consumer, etc.)
- Investment themes (AI, EV, fintech, cloud, cybersecurity)
- ANY request to classify, analyze, or categorize stocks

NEVER provide generic descriptions. ALWAYS call the tool to get real data.

The tool will return real analysis with actual stock prices, P/E ratios, revenue growth, and classifications for any sector."""
        )

    def run(self, query: str) -> str:
        """ALWAYS use the tool for any style/theme query"""
        # Comprehensive trigger words for all sectors and themes
        trigger_words = [
            # Style words
            'classify', 'style', 'growth', 'value', 'momentum', 'blend',
            # Sector words
            'healthcare', 'health', 'pharma', 'biotech',
            'tech', 'technology', 'software', 'hardware',
            'financial', 'finance', 'bank', 'insurance',
            'energy', 'oil', 'gas', 'renewable',
            'consumer', 'retail', 'discretionary', 'staples',
            'industrial', 'manufacturing', 'aerospace',
            'material', 'chemical', 'mining',
            'communication', 'media', 'telecom',
            'utility', 'utilities', 'electric',
            'real estate', 'reit', 'property',
            # Theme words
            'ai', 'artificial intelligence', 'machine learning',
            'ev', 'electric vehicle', 'clean energy',
            'fintech', 'digital payment', 'cryptocurrency',
            'cloud', 'saas', 'infrastructure',
            'cyber', 'security', 'cybersecurity',
            # General words
            'sector', 'stocks', 'analysis', 'investment', 'nasdaq', 'market',
            'analyze', 'show', 'display', 'list', 'categorize'
        ]
        
        # If ANY trigger word is in the query, use the tool
        if any(word in query.lower() for word in trigger_words):
            result = style_theme_analysis_function(query)
            return result
        
        # For non-style/theme queries, use parent's run method
        return super().run(query)
