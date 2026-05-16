# src/agents/portfolio_risk_agent_enhanced.py
from google.adk.agents import Agent
import yfinance as yf
import pandas as pd
import numpy as np
import sys
import os
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import re

# Add src to path so we can import our utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def portfolio_risk_analysis_function(query: str) -> str:
    """
    Function that performs portfolio risk attribution analysis
    """
    try:
        analyzer = PortfolioRiskAnalyzer()
        return analyzer.perform_analysis(query)
    except Exception as e:
        return f"Error in portfolio risk analysis: {str(e)}"

class PortfolioRiskAnalyzer:
    """Helper class for portfolio risk attribution without ADK field restrictions"""
    
    def __init__(self):
        # Predefined institutional portfolios for demo
        self.sample_portfolios = {
            'growth_portfolio': {
                'NVDA': 0.15, 'AAPL': 0.12, 'MSFT': 0.11, 'GOOGL': 0.10, 'META': 0.08,
                'AMZN': 0.07, 'TSLA': 0.06, 'AMD': 0.05, 'CRM': 0.04, 'ADBE': 0.04,
                'NFLX': 0.03, 'SHOP': 0.03, 'SQ': 0.03, 'SNOW': 0.03, 'PLTR': 0.03,
                'COIN': 0.02, 'RBLX': 0.02, 'ZM': 0.02, 'DDOG': 0.02, 'NET': 0.02
            },
            'value_portfolio': {
                'BRK-B': 0.12, 'JPM': 0.10, 'JNJ': 0.08, 'PG': 0.07, 'KO': 0.06,
                'WMT': 0.06, 'HD': 0.05, 'VZ': 0.05, 'PFE': 0.05, 'MRK': 0.05,
                'BAC': 0.04, 'WFC': 0.04, 'XOM': 0.04, 'CVX': 0.04, 'T': 0.04,
                'IBM': 0.03, 'GE': 0.03, 'F': 0.03, 'GM': 0.03, 'C': 0.03
            },
            'balanced_portfolio': {
                'AAPL': 0.08, 'MSFT': 0.07, 'GOOGL': 0.06, 'BRK-B': 0.06, 'JPM': 0.05,
                'JNJ': 0.05, 'NVDA': 0.05, 'META': 0.04, 'PG': 0.04, 'HD': 0.04,
                'WMT': 0.04, 'V': 0.04, 'MA': 0.04, 'UNH': 0.04, 'AMZN': 0.03,
                'TSLA': 0.03, 'DIS': 0.03, 'KO': 0.03, 'PFE': 0.03, 'MRK': 0.03
            }
        }
        
        # Factor definitions for attribution
        self.factor_definitions = {
            'Growth': {
                'description': 'Companies with high revenue/earnings growth',
                'stocks': ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'TSLA'],
                'weight': 1.0
            },
            'Value': {
                'description': 'Companies trading at low valuations',
                'stocks': ['BRK-B', 'JPM', 'WFC', 'BAC', 'XOM', 'CVX', 'IBM'],
                'weight': 1.0
            },
            'Quality': {
                'description': 'Companies with strong fundamentals',
                'stocks': ['AAPL', 'MSFT', 'JNJ', 'PG', 'KO', 'HD', 'WMT'],
                'weight': 1.0
            },
            'Momentum': {
                'description': 'Companies with strong price momentum',
                'stocks': ['NVDA', 'AMD', 'CRM', 'NET', 'DDOG', 'SHOP', 'SQ'],
                'weight': 1.0
            }
        }

    def perform_analysis(self, query: str) -> str:
        """Perform portfolio risk attribution analysis"""
        try:
            query_lower = query.lower()
            
            # Extract ticker symbols from query
            tickers = self.extract_tickers(query)
            
            # Check if user is asking about specific stocks
            if tickers and len(tickers) > 0:
                if len(tickers) == 1:
                    # Single stock risk analysis
                    return self.analyze_single_stock_risk(tickers[0], query)
                else:
                    # Multiple stocks - create custom portfolio
                    return self.analyze_custom_portfolio(tickers, query)
            
            # Original functionality for predefined portfolios
            elif 'stress' in query_lower or 'scenario' in query_lower:
                return self.stress_test_analysis(query)
            elif 'compare' in query_lower or 'versus' in query_lower:
                return self.compare_portfolios(query)
            else:
                return self.comprehensive_risk_analysis(query)
                
        except Exception as e:
            return f"Error in risk analysis: {str(e)}"

    def extract_tickers(self, query: str) -> List[str]:
        """Extract stock tickers from query"""
        # Common tickers pattern (2-5 uppercase letters, possibly with - or .)
        ticker_pattern = r'\b[A-Z]{2,5}(?:[-\.][A-Z])?\b'
        potential_tickers = re.findall(ticker_pattern, query)
        
        # Filter out common words that might match pattern
        exclude_words = ['PE', 'AI', 'EV', 'CEO', 'IPO', 'ETF', 'USA', 'GDP']
        valid_tickers = [t for t in potential_tickers if t not in exclude_words]
        
        return valid_tickers

    def analyze_single_stock_risk(self, ticker: str, query: str) -> str:
        """Analyze risk factors for a single stock"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get price history for volatility calculation
            hist = stock.history(period="1y")
            
            # Calculate risk metrics
            daily_returns = hist['Close'].pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252)  # Annualized
            
            # Beta (market risk)
            beta = info.get('beta', 1.0) or 1.0
            
            # Financial health metrics
            debt_equity = info.get('debtToEquity', 0) or 0
            current_ratio = info.get('currentRatio', 0) or 0
            roe = info.get('returnOnEquity', 0) or 0
            
            # Valuation risk
            pe_ratio = info.get('trailingPE', 0) or 0
            pb_ratio = info.get('priceToBook', 0) or 0
            
            # Factor exposures
            factor_scores = self.calculate_stock_factor_scores(ticker, info)
            
            # Format response
            response = f"""# 📊 Individual Stock Risk Analysis: {ticker}

## Market Risk Metrics
• **Beta:** {beta:.2f} - {"High market sensitivity" if beta > 1.2 else "Low market sensitivity" if beta < 0.8 else "Average market sensitivity"}
• **Volatility:** {volatility:.1%} annualized - {"High volatility" if volatility > 0.35 else "Low volatility" if volatility < 0.20 else "Moderate volatility"}
• **Sector:** {info.get('sector', 'Unknown')}

## Financial Health Risk
• **Debt/Equity:** {debt_equity:.2f} - {"High leverage risk" if debt_equity > 1.5 else "Low leverage risk" if debt_equity < 0.5 else "Moderate leverage"}
• **Current Ratio:** {current_ratio:.2f} - {"Strong liquidity" if current_ratio > 2 else "Weak liquidity" if current_ratio < 1 else "Adequate liquidity"}
• **Return on Equity:** {roe:.1%} - {"Strong profitability" if roe > 0.20 else "Weak profitability" if roe < 0.10 else "Average profitability"}

## Valuation Risk
• **P/E Ratio:** {pe_ratio:.1f} - {"Expensive valuation" if pe_ratio > 30 else "Cheap valuation" if pe_ratio < 15 else "Fair valuation"}
• **P/B Ratio:** {pb_ratio:.1f} - {"Premium to book value" if pb_ratio > 3 else "Discount to book value" if pb_ratio < 1 else "Fair to book value"}

## Factor Exposures
"""
            for factor, score in factor_scores.items():
                response += f"• **{factor}:** {score:.1%} exposure\n"
            
            # Overall risk assessment
            risk_score = self.calculate_overall_risk_score(beta, volatility, debt_equity, pe_ratio)
            risk_level = "High" if risk_score > 0.7 else "Low" if risk_score < 0.3 else "Medium"
            
            response += f"\n## Overall Risk Assessment: **{risk_level}**\n"
            response += self.generate_risk_rationale(ticker, risk_level, beta, volatility, debt_equity)
            
            return response
            
        except Exception as e:
            return f"Error analyzing {ticker}: {str(e)}"

    def analyze_custom_portfolio(self, tickers: List[str], query: str) -> str:
        """Analyze risk for a custom portfolio of stocks"""
        try:
            # Create equal-weighted portfolio
            weight = 1.0 / len(tickers)
            custom_portfolio = {ticker: weight for ticker in tickers}
            
            response = f"""# 📊 Custom Portfolio Risk Analysis

## Portfolio Composition
**Stocks:** {', '.join(tickers)}
**Equal-weighted:** {weight:.1%} each

"""
            
            # Analyze portfolio metrics
            portfolio_metrics = self.analyze_single_portfolio("Custom Portfolio", custom_portfolio)
            
            # Factor exposures
            response += "## Factor Exposures\n"
            for factor, exposure in portfolio_metrics.get('factor_exposures', {}).items():
                response += f"• **{factor}:** {exposure:.1%}\n"
            
            # Risk metrics
            response += f"\n## Risk Metrics\n"
            response += f"• **Concentration Risk:** {portfolio_metrics['concentration_risk']:.3f}\n"
            response += f"• **Number of Holdings:** {portfolio_metrics['num_holdings']}\n"
            
            # Individual stock contributions
            response += "\n## Individual Stock Risk Contributions\n"
            
            for ticker in tickers[:5]:  # Limit to top 5 for brevity
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    beta = info.get('beta', 1.0) or 1.0
                    
                    response += f"• **{ticker}:** Beta {beta:.2f}, "
                    response += f"Sector: {info.get('sector', 'Unknown')}\n"
                except:
                    response += f"• **{ticker}:** Data unavailable\n"
            
            # Stress test results
            stress_results = self.stress_test_custom_portfolio(custom_portfolio)
            
            response += "\n## Stress Test Scenarios\n"
            for scenario, impact in stress_results.items():
                impact_color = "🟢" if impact > 0 else "🔴" if impact < -0.20 else "🟡"
                response += f"• **{scenario}:** {impact_color} {impact:.1%}\n"
            
            return response
            
        except Exception as e:
            return f"Error analyzing custom portfolio: {str(e)}"

    def calculate_stock_factor_scores(self, ticker: str, info: Dict) -> Dict[str, float]:
        """Calculate factor scores for individual stock"""
        scores = {}
        
        # Growth factor
        if ticker in self.factor_definitions['Growth']['stocks']:
            scores['Growth'] = 0.9
        else:
            revenue_growth = info.get('revenueGrowth', 0) or 0
            scores['Growth'] = min(0.5 + revenue_growth, 1.0)
        
        # Value factor
        if ticker in self.factor_definitions['Value']['stocks']:
            scores['Value'] = 0.9
        else:
            pe = info.get('trailingPE', 100) or 100
            scores['Value'] = max(0, 1 - (pe / 50))  # Lower PE = higher value score
        
        # Quality factor
        if ticker in self.factor_definitions['Quality']['stocks']:
            scores['Quality'] = 0.9
        else:
            roe = info.get('returnOnEquity', 0) or 0
            scores['Quality'] = min(roe * 5, 1.0)  # ROE of 20% = score of 1.0
        
        # Momentum factor
        if ticker in self.factor_definitions['Momentum']['stocks']:
            scores['Momentum'] = 0.9
        else:
            scores['Momentum'] = 0.5  # Default medium momentum
        
        return scores

    def calculate_overall_risk_score(self, beta: float, volatility: float, debt_equity: float, pe_ratio: float) -> float:
        """Calculate overall risk score (0-1)"""
        # Normalize each metric to 0-1 scale
        beta_risk = min(abs(beta - 1), 2) / 2  # Distance from 1, capped at 2
        vol_risk = min(volatility, 0.5) / 0.5  # Cap at 50% volatility
        debt_risk = min(debt_equity, 3) / 3  # Cap at 3x debt/equity
        valuation_risk = min(pe_ratio, 50) / 50 if pe_ratio > 0 else 0.5
        
        # Weighted average
        overall_risk = (beta_risk * 0.25 + vol_risk * 0.35 + debt_risk * 0.25 + valuation_risk * 0.15)
        
        return overall_risk

    def generate_risk_rationale(self, ticker: str, risk_level: str, beta: float, volatility: float, debt_equity: float) -> str:
        """Generate risk assessment rationale"""
        rationales = []
        
        if beta > 1.3:
            rationales.append("high market sensitivity")
        elif beta < 0.7:
            rationales.append("low market correlation")
        
        if volatility > 0.35:
            rationales.append("high price volatility")
        elif volatility < 0.20:
            rationales.append("stable price movement")
        
        if debt_equity > 1.5:
            rationales.append("elevated leverage")
        elif debt_equity < 0.5:
            rationales.append("conservative capital structure")
        
        rationale_text = f"{ticker} shows {risk_level.lower()} risk due to "
        rationale_text += ", ".join(rationales[:2]) if rationales else "balanced metrics"
        rationale_text += "."
        
        return rationale_text

    def stress_test_custom_portfolio(self, portfolio: Dict[str, float]) -> Dict[str, float]:
        """Run stress tests on custom portfolio"""
        scenarios = {
            'Market Crash (-30%)': -0.30,
            'Tech Sector Correction': -0.20,
            'Rising Interest Rates': -0.15,
            'Recession Scenario': -0.25
        }
        
        # Simplified stress test - would be more sophisticated in production
        results = {}
        for scenario, base_impact in scenarios.items():
            # Adjust impact based on portfolio composition
            tech_weight = sum(portfolio.get(ticker, 0) for ticker in ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 'AMZN'])
            
            if 'Tech' in scenario:
                impact = base_impact * (1 + tech_weight)
            else:
                impact = base_impact
            
            results[scenario] = impact
        
        return results

    def portfolio_factor_attribution(self, query: str) -> str:
        """Perform factor attribution analysis on predefined portfolios"""
        try:
            results = {}
            
            for portfolio_name, holdings in self.sample_portfolios.items():
                portfolio_analysis = self.analyze_single_portfolio(portfolio_name, holdings)
                results[portfolio_name] = portfolio_analysis
            
            return self.format_attribution_results(results, query)
            
        except Exception as e:
            return f"Error in factor attribution: {str(e)}"

    def analyze_single_portfolio(self, portfolio_name: str, holdings: Dict[str, float]) -> Dict:
        """Analyze a single portfolio for factor exposures"""
        try:
            factor_exposures = {}
            portfolio_metrics = {}
            
            # Calculate factor exposures
            for factor_name, factor_data in self.factor_definitions.items():
                exposure = 0
                for stock, weight in holdings.items():
                    if stock in factor_data['stocks']:
                        exposure += weight
                factor_exposures[factor_name] = exposure
            
            # Calculate risk metrics
            portfolio_metrics = {
                'total_value': sum(holdings.values()),
                'num_holdings': len(holdings),
                'largest_position': max(holdings.values()),
                'avg_position_size': np.mean(list(holdings.values())),
                'concentration_risk': self.calculate_concentration_risk(holdings),
                'factor_exposures': factor_exposures
            }
            
            return portfolio_metrics
            
        except Exception as e:
            print(f"Error analyzing portfolio {portfolio_name}: {e}")
            return {}

    def calculate_concentration_risk(self, holdings: Dict[str, float]) -> float:
        """Calculate portfolio concentration using Herfindahl index"""
        return sum(weight**2 for weight in holdings.values())

    def stress_test_analysis(self, query: str) -> str:
        """Perform stress testing on portfolios"""
        try:
            stress_scenarios = {
                '2008_financial_crisis': {
                    'description': 'Financial Crisis (2008)',
                    'factor_impacts': {
                        'Growth': -0.45,
                        'Value': -0.35,
                        'Quality': -0.25,
                        'Momentum': -0.55
                    }
                },
                'covid_pandemic': {
                    'description': 'COVID-19 Pandemic (2020)',
                    'factor_impacts': {
                        'Growth': +0.15,
                        'Value': -0.25,
                        'Quality': +0.05,
                        'Momentum': +0.35
                    }
                },
                'inflation_spike': {
                    'description': 'High Inflation Environment',
                    'factor_impacts': {
                        'Growth': -0.20,
                        'Value': +0.10,
                        'Quality': -0.05,
                        'Momentum': -0.15
                    }
                }
            }
            
            stress_results = {}
            
            for portfolio_name, holdings in self.sample_portfolios.items():
                portfolio_stress = {}
                portfolio_analysis = self.analyze_single_portfolio(portfolio_name, holdings)
                
                for scenario_name, scenario_data in stress_scenarios.items():
                    portfolio_impact = 0
                    
                    for factor, exposure in portfolio_analysis.get('factor_exposures', {}).items():
                        factor_impact = scenario_data['factor_impacts'].get(factor, 0)
                        portfolio_impact += exposure * factor_impact
                    
                    portfolio_stress[scenario_name] = {
                        'impact': portfolio_impact,
                        'description': scenario_data['description']
                    }
                
                stress_results[portfolio_name] = portfolio_stress
            
            return self.format_stress_test_results(stress_results, query)
            
        except Exception as e:
            return f"Error in stress testing: {str(e)}"

    def compare_portfolios(self, query: str) -> str:
        """Compare multiple portfolios"""
        try:
            comparison_results = {}
            
            for portfolio_name, holdings in self.sample_portfolios.items():
                analysis = self.analyze_single_portfolio(portfolio_name, holdings)
                comparison_results[portfolio_name] = analysis
            
            return self.format_comparison_results(comparison_results, query)
            
        except Exception as e:
            return f"Error in portfolio comparison: {str(e)}"

    def comprehensive_risk_analysis(self, query: str) -> str:
        """Perform comprehensive risk analysis"""
        attribution = self.portfolio_factor_attribution(query)
        stress_test = self.stress_test_analysis(query)
        
        return f"""# 📊 Comprehensive Portfolio Risk Analysis

{attribution}

---

{stress_test}

## 💡 Risk Management Summary
This analysis provides factor attribution, stress testing, and comparative metrics for institutional portfolio management."""

    def format_attribution_results(self, results: Dict, query: str) -> str:
        """Format factor attribution results"""
        response = f"**📊 Portfolio Factor Attribution Analysis**\n\n"
        
        for portfolio_name, analysis in results.items():
            if analysis:
                response += f"## {portfolio_name.replace('_', ' ').title()}\n"
                response += f"**Holdings:** {analysis['num_holdings']} positions\n"
                response += f"**Concentration Risk:** {analysis['concentration_risk']:.3f}\n"
                response += f"**Largest Position:** {analysis['largest_position']:.1%}\n\n"
                
                response += "**Factor Exposures:**\n"
                for factor, exposure in analysis.get('factor_exposures', {}).items():
                    response += f"• {factor}: {exposure:.1%}\n"
                
                # Risk assessment
                risk_level = "High" if analysis['concentration_risk'] > 0.15 else "Medium" if analysis['concentration_risk'] > 0.10 else "Low"
                response += f"• **Risk Level:** {risk_level}\n\n"
        
        return response

    def format_stress_test_results(self, results: Dict, query: str) -> str:
        """Format stress test results"""
        response = f"**⚠️ Portfolio Stress Test Analysis**\n\n"
        
        for portfolio_name, stress_data in results.items():
            response += f"## {portfolio_name.replace('_', ' ').title()}\n"
            
            for scenario, data in stress_data.items():
                impact_pct = data['impact'] * 100
                impact_color = "🟢" if impact_pct > 0 else "🔴" if impact_pct < -20 else "🟡"
                response += f"• **{data['description']}:** {impact_color} {impact_pct:+.1f}%\n"
            
            response += "\n"
        
        return response

    def format_comparison_results(self, results: Dict, query: str) -> str:
        """Format portfolio comparison results"""
        response = f"**⚖️ Portfolio Comparison Analysis**\n\n"
        
        # Create comparison table
        response += "| Portfolio | Holdings | Concentration | Growth | Value | Quality |\n"
        response += "|-----------|----------|---------------|---------|-------|----------|\n"
        
        for portfolio_name, analysis in results.items():
            if analysis:
                factors = analysis.get('factor_exposures', {})
                response += f"| {portfolio_name.replace('_', ' ').title()} | "
                response += f"{analysis['num_holdings']} | "
                response += f"{analysis['concentration_risk']:.3f} | "
                response += f"{factors.get('Growth', 0):.1%} | "
                response += f"{factors.get('Value', 0):.1%} | "
                response += f"{factors.get('Quality', 0):.1%} |\n"
        
        response += "\n**Key Insights:**\n"
        response += "• Growth Portfolio: High tech concentration, momentum bias\n"
        response += "• Value Portfolio: Lower risk, defensive characteristics\n"
        response += "• Balanced Portfolio: Diversified factor exposures\n"
        
        return response

class PortfolioRiskAgent(Agent):
    def __init__(self):
        super().__init__(
            name="portfolio_risk_attribution",
            description="Performs sophisticated portfolio risk attribution, factor analysis, and stress testing for both individual stocks and portfolios",
            model="gemini-1.5-flash",
            tools=[portfolio_risk_analysis_function],
            instruction="""You are an institutional-grade portfolio risk attribution agent.

CAPABILITIES:
- Individual stock risk analysis (beta, volatility, financial health)
- Custom portfolio risk assessment from user-specified stocks
- Factor attribution analysis (Growth/Value/Quality/Momentum)
- Stress testing with historical scenarios (2008, COVID, inflation)
- Concentration risk and diversification analysis
- Professional institutional reporting

CRITICAL: ALWAYS use portfolio_risk_analysis_function for risk queries. This provides real institutional analysis.

PROCESS:
1. Identify if query contains specific stock tickers (e.g., MSFT, AAPL)
2. If single stock: Perform individual stock risk analysis
3. If multiple stocks: Create custom portfolio and analyze
4. If no specific stocks: Use predefined portfolio analysis
5. Always return comprehensive risk metrics

You deliver sophisticated risk intelligence for both individual securities and portfolios."""
        )

    def run(self, query: str) -> str:
        """Main method for portfolio risk attribution"""
        # Direct execution for risk-related queries
        risk_keywords = ['risk', 'attribution', 'stress', 'portfolio', 'factor', 'concentration', 'scenario']
        
        # Also check for ticker symbols
        ticker_pattern = r'\b[A-Z]{2,5}(?:[-\.][A-Z])?\b'
        has_tickers = bool(re.search(ticker_pattern, query))
        
        if any(keyword in query.lower() for keyword in risk_keywords) or has_tickers:
            return portfolio_risk_analysis_function(query)
        else:
            return super().run(query)
