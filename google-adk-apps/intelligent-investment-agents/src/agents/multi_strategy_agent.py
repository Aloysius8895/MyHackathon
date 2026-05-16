# src/agents/multi_strategy_agent.py - FIXED VERSION
from google.adk.agents import Agent
import yfinance as yf
import pandas as pd
import numpy as np
import sys
import os
from typing import Dict, List, Tuple, Set
from datetime import datetime, timedelta

# Add src to path so we can import our utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def multi_strategy_analysis_function(query: str) -> str:
    """
    Function that performs multi-strategy portfolio monitoring and analysis
    """
    try:
        analyzer = MultiStrategyAnalyzer()
        return analyzer.perform_analysis(query)
    except Exception as e:
        return f"Error in multi-strategy analysis: {str(e)}"

class MultiStrategyAnalyzer:
    """Helper class for multi-strategy portfolio monitoring without ADK field restrictions"""
    
    def __init__(self):
        # Institutional investment managers with different strategies
        self.institutional_portfolios = {
            'growth_manager_a': {
                'name': 'TechGrowth Capital',
                'strategy': 'Technology Growth',
                'aum': 2500000000,  # $2.5B AUM
                'holdings': {
                    'NVDA': 0.18, 'AAPL': 0.15, 'MSFT': 0.13, 'GOOGL': 0.12, 'META': 0.10,
                    'AMZN': 0.08, 'TSLA': 0.07, 'AMD': 0.06, 'CRM': 0.05, 'ADBE': 0.04,
                    'NFLX': 0.02
                }
            },
            'growth_manager_b': {
                'name': 'Innovation Partners',
                'strategy': 'Innovation Growth',
                'aum': 1800000000,  # $1.8B AUM
                'holdings': {
                    'MSFT': 0.16, 'GOOGL': 0.14, 'NVDA': 0.12, 'META': 0.11, 'AAPL': 0.10,
                    'AMZN': 0.09, 'ADBE': 0.07, 'CRM': 0.06, 'SNOW': 0.05, 'PLTR': 0.04,
                    'DDOG': 0.03, 'NET': 0.03
                }
            },
            'value_manager_a': {
                'name': 'Berkshire-Style Value',
                'strategy': 'Deep Value',
                'aum': 3200000000,  # $3.2B AUM
                'holdings': {
                    'BRK-B': 0.20, 'JPM': 0.15, 'JNJ': 0.12, 'PG': 0.10, 'KO': 0.08,
                    'WMT': 0.07, 'HD': 0.06, 'VZ': 0.05, 'PFE': 0.05, 'MRK': 0.05,
                    'BAC': 0.04, 'WFC': 0.03
                }
            },
            'balanced_manager': {
                'name': 'Diversified Alpha',
                'strategy': 'Balanced Growth',
                'aum': 4500000000,  # $4.5B AUM
                'holdings': {
                    'AAPL': 0.10, 'MSFT': 0.09, 'GOOGL': 0.08, 'BRK-B': 0.07, 'JPM': 0.06,
                    'JNJ': 0.06, 'NVDA': 0.06, 'META': 0.05, 'PG': 0.05, 'HD': 0.05,
                    'WMT': 0.05, 'V': 0.04, 'MA': 0.04, 'UNH': 0.04, 'AMZN': 0.04,
                    'TSLA': 0.03, 'DIS': 0.03, 'KO': 0.03, 'PFE': 0.03, 'MRK': 0.03,
                    'CVX': 0.02, 'XOM': 0.02
                }
            },
            'momentum_manager': {
                'name': 'Trend Followers',
                'strategy': 'Momentum',
                'aum': 1200000000,  # $1.2B AUM
                'holdings': {
                    'NVDA': 0.25, 'AMD': 0.15, 'TSLA': 0.12, 'COIN': 0.08, 'RBLX': 0.07,
                    'SHOP': 0.06, 'SQ': 0.05, 'SNOW': 0.05, 'NET': 0.04, 'DDOG': 0.04,
                    'PLTR': 0.04, 'ROKU': 0.03, 'ZM': 0.02
                }
            }
        }
        
        # Sector classifications for analysis
        self.sector_mapping = {
            'Technology': ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 'AMZN', 'ADBE', 'CRM', 'ORCL', 'INTC', 'AMD'],
            'Healthcare': ['JNJ', 'PFE', 'MRK', 'UNH', 'ABBV', 'TMO', 'ABT', 'CVS', 'AMGN', 'MDT'],
            'Financials': ['BRK-B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'GS', 'MS', 'AXP', 'SCHW'],
            'Consumer': ['HD', 'WMT', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'COST', 'TJX', 'DG'],
            'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'VLO', 'PSX', 'OXY', 'PXD'],
            'Communication': ['DIS', 'NFLX', 'CMCSA', 'VZ', 'T', 'TMUS', 'CHTR'],
            'Other': ['KO', 'PG', 'TSLA', 'COIN', 'RBLX', 'SHOP', 'SQ', 'SNOW', 'NET', 'DDOG', 'PLTR', 'ROKU', 'ZM']
        }

    def perform_analysis(self, query: str) -> str:
        """Perform multi-strategy analysis based on query type"""
        try:
            query_lower = query.lower()
            
            if 'overlap' in query_lower or 'redundant' in query_lower:
                return self.analyze_manager_overlap()
            elif 'correlation' in query_lower or 'correlated' in query_lower:
                return self.analyze_portfolio_correlations()
            elif 'concentration' in query_lower or 'risk' in query_lower:
                return self.analyze_concentration_risk()
            elif 'performance' in query_lower or 'compare' in query_lower:
                return self.compare_manager_performance()
            elif 'sector' in query_lower or 'allocation' in query_lower:
                return self.analyze_sector_allocations()
            else:
                return self.comprehensive_multi_strategy_analysis()
                
        except Exception as e:
            return f"Error in multi-strategy analysis: {str(e)}"

    def analyze_manager_overlap(self) -> str:
        """Analyze holding overlaps between managers"""
        response = "# 🎭 Manager Overlap Analysis\n\n"
        response += "**Identifying redundant holdings across investment managers**\n\n"
        
        # Find all unique holdings
        all_holdings = set()
        for manager_data in self.institutional_portfolios.values():
            all_holdings.update(manager_data['holdings'].keys())
        
        # Analyze overlap for each stock
        overlap_analysis = {}
        for stock in all_holdings:
            managers_holding = []
            total_weight = 0
            
            for manager_id, manager_data in self.institutional_portfolios.items():
                if stock in manager_data['holdings']:
                    weight = manager_data['holdings'][stock]
                    managers_holding.append({
                        'manager': manager_data['name'],
                        'strategy': manager_data['strategy'],
                        'weight': weight,
                        'dollar_value': weight * manager_data['aum']
                    })
                    total_weight += weight
            
            if len(managers_holding) > 1:  # Only stocks held by multiple managers
                overlap_analysis[stock] = {
                    'managers': managers_holding,
                    'overlap_count': len(managers_holding),
                    'total_weight': total_weight,
                    'total_value': sum(m['dollar_value'] for m in managers_holding)
                }
        
        # Sort by overlap severity (number of managers + total value)
        sorted_overlaps = sorted(
            overlap_analysis.items(),
            key=lambda x: x[1]['overlap_count'] * x[1]['total_value'],
            reverse=True
        )
        
        response += "## High Overlap Holdings\n\n"
        for stock, data in sorted_overlaps[:8]:  # Show top 8
            response += f"### {stock}\n"
            response += f"**Held by {data['overlap_count']} managers** | **Total Value: ${data['total_value']/1e9:.2f}B**\n\n"
            
            for manager in data['managers']:
                response += f"• **{manager['manager']}**: {manager['weight']:.1%} (${manager['dollar_value']/1e6:.0f}M)\n"
            
            response += f"• **Overlap Risk:** High concentration across {data['overlap_count']} strategies\n\n"
        
        # Summary statistics
        total_overlapping_stocks = len(overlap_analysis)
        high_overlap_stocks = len([s for s in overlap_analysis.values() if s['overlap_count'] >= 3])
        
        response += "## 📊 Overlap Summary\n\n"
        response += f"• **Total Overlapping Holdings:** {total_overlapping_stocks} stocks\n"
        response += f"• **High Overlap (3+ managers):** {high_overlap_stocks} stocks\n"
        response += f"• **Platform Total Holdings:** {len(all_holdings)} unique stocks\n"
        
        return response

    def analyze_portfolio_correlations(self) -> str:
        """Analyze correlations between different manager portfolios"""
        response = "# 📈 Portfolio Correlation Analysis\n\n"
        response += "**Measuring how similarly different managers' portfolios are structured**\n\n"
        
        # Calculate portfolio correlations based on overlapping holdings
        managers = list(self.institutional_portfolios.keys())
        correlation_matrix = {}
        
        for manager1 in managers:
            correlation_matrix[manager1] = {}
            for manager2 in managers:
                if manager1 == manager2:
                    correlation_matrix[manager1][manager2] = 1.0
                else:
                    correlation = self.calculate_portfolio_correlation(manager1, manager2)
                    correlation_matrix[manager1][manager2] = correlation
        
        # Display correlation matrix
        response += "## Correlation Matrix\n\n"
        response += "| Manager | Tech Growth | Innovation | Value | Balanced | Momentum |\n"
        response += "|---------|-------------|------------|-------|----------|----------|\n"
        
        manager_short_names = {
            'growth_manager_a': 'Tech Growth',
            'growth_manager_b': 'Innovation', 
            'value_manager_a': 'Value',
            'balanced_manager': 'Balanced',
            'momentum_manager': 'Momentum'
        }
        
        for manager1 in managers:
            row = f"| {manager_short_names[manager1]} |"
            for manager2 in managers:
                corr = correlation_matrix[manager1][manager2]
                row += f" {corr:.2f} |"
            response += row + "\n"
        
        response += "\n"
        
        # Identify high correlation pairs
        response += "## 🔗 Key Correlation Insights\n\n"
        
        # Find highest correlation pair (excluding self-correlation)
        max_corr = 0
        max_pair = None
        
        for manager1 in managers:
            for manager2 in managers:
                if manager1 != manager2:
                    corr = correlation_matrix[manager1][manager2]
                    if corr > max_corr:
                        max_corr = corr
                        max_pair = (manager1, manager2)
        
        if max_pair:
            m1_data = self.institutional_portfolios[max_pair[0]]
            m2_data = self.institutional_portfolios[max_pair[1]]
            response += f"• **Highest Correlation:** {m1_data['name']} ↔ {m2_data['name']} ({max_corr:.2f})\n"
        
        # Calculate average correlation
        all_correlations = [
            correlation_matrix[m1][m2] for m1 in managers for m2 in managers if m1 != m2
        ]
        avg_correlation = np.mean(all_correlations) if all_correlations else 0
        
        response += f"• **Average Cross-Manager Correlation:** {avg_correlation:.2f}\n"
        
        if avg_correlation < 0.3:
            response += "• **Assessment:** ✅ Excellent diversification across managers\n"
        elif avg_correlation < 0.5:
            response += "• **Assessment:** 🟡 Good diversification with some overlap\n"
        else:
            response += "• **Assessment:** 🔴 Consider reducing manager overlap\n"
        
        return response

    def calculate_portfolio_correlation(self, manager1: str, manager2: str) -> float:
        """Calculate correlation between two portfolios based on overlapping holdings"""
        portfolio1 = self.institutional_portfolios[manager1]['holdings']
        portfolio2 = self.institutional_portfolios[manager2]['holdings']
        
        # Find common holdings
        common_stocks = set(portfolio1.keys()) & set(portfolio2.keys())
        
        if len(common_stocks) < 2:
            return 0.0  # Need at least 2 common holdings for meaningful correlation
        
        # Calculate overlap-based correlation
        overlap_weight = sum(min(portfolio1.get(stock, 0), portfolio2.get(stock, 0)) for stock in common_stocks)
        total_weight1 = sum(portfolio1.values())
        total_weight2 = sum(portfolio2.values())
        
        # Normalized correlation score
        correlation = overlap_weight / min(total_weight1, total_weight2)
        return min(correlation, 1.0)

    def analyze_concentration_risk(self) -> str:
        """Analyze concentration risks across the multi-manager platform"""
        response = "# ⚠️ Multi-Manager Concentration Risk Analysis\n\n"
        
        # Aggregate holdings across all managers
        aggregate_holdings = {}
        total_aum = sum(manager['aum'] for manager in self.institutional_portfolios.values())
        
        for manager_data in self.institutional_portfolios.values():
            for stock, weight in manager_data['holdings'].items():
                dollar_amount = weight * manager_data['aum']
                if stock in aggregate_holdings:
                    aggregate_holdings[stock] += dollar_amount
                else:
                    aggregate_holdings[stock] = dollar_amount
        
        # Convert to percentages of total AUM
        aggregate_percentages = {
            stock: amount / total_aum for stock, amount in aggregate_holdings.items()
        }
        
        # Sort by concentration
        sorted_concentrations = sorted(
            aggregate_percentages.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        response += f"**Total Platform AUM:** ${total_aum/1e9:.1f}B across 5 managers\n\n"
        
        response += "## Top Platform Concentrations\n\n"
        for i, (stock, percentage) in enumerate(sorted_concentrations[:10], 1):
            dollar_value = aggregate_holdings[stock]
            response += f"{i}. **{stock}**: {percentage:.2%} (${dollar_value/1e9:.2f}B)\n"
        
        # Risk analysis
        response += "\n## 🎯 Concentration Risk Assessment\n\n"
        
        top_10_concentration = sum(pct for _, pct in sorted_concentrations[:10])
        top_5_concentration = sum(pct for _, pct in sorted_concentrations[:5])
        single_stock_max = sorted_concentrations[0][1] if sorted_concentrations else 0
        
        response += f"• **Top 5 Holdings:** {top_5_concentration:.1%} of total AUM\n"
        response += f"• **Top 10 Holdings:** {top_10_concentration:.1%} of total AUM\n"
        response += f"• **Largest Single Position:** {single_stock_max:.2%}\n\n"
        
        # Risk levels
        if single_stock_max > 0.08:  # 8%
            response += "🔴 **HIGH RISK:** Single stock concentration exceeds 8%\n"
        elif single_stock_max > 0.05:  # 5%
            response += "🟡 **MEDIUM RISK:** Single stock concentration 5-8%\n"
        else:
            response += "🟢 **LOW RISK:** Well-diversified single stock positions\n"
        
        return response

    def compare_manager_performance(self) -> str:
        """Compare performance characteristics across managers"""
        response = "# 📊 Manager Performance Comparison\n\n"
        
        response += "## Manager Overview\n\n"
        response += "| Manager | Strategy | AUM | Holdings | Concentration |\n"
        response += "|---------|----------|-----|----------|---------------|\n"
        
        for manager_id, manager_data in self.institutional_portfolios.items():
            aum_billions = manager_data['aum'] / 1e9
            num_holdings = len(manager_data['holdings'])
            # Calculate Herfindahl concentration index
            concentration = sum(weight**2 for weight in manager_data['holdings'].values())
            
            response += f"| {manager_data['name']} | {manager_data['strategy']} | ${aum_billions:.1f}B | {num_holdings} | {concentration:.3f} |\n"
        
        response += "\n## 🎯 Strategy Risk Profiles\n\n"
        
        for manager_id, manager_data in self.institutional_portfolios.items():
            holdings = manager_data['holdings']
            concentration = sum(weight**2 for weight in holdings.values())
            max_position = max(holdings.values()) if holdings else 0
            
            response += f"### {manager_data['name']}\n"
            response += f"- **Strategy:** {manager_data['strategy']}\n"
            response += f"- **Largest Position:** {max_position:.1%}\n"
            response += f"- **Risk Profile:** {'High' if concentration > 0.15 else 'Medium' if concentration > 0.10 else 'Low'}\n\n"
        
        return response

    def analyze_sector_allocations(self) -> str:
        """Analyze sector allocations across all managers"""
        response = "# 🏢 Cross-Manager Sector Analysis\n\n"
        
        # Calculate platform-wide sector exposure
        total_aum = sum(manager['aum'] for manager in self.institutional_portfolios.values())
        platform_sector_exposure = {sector: 0.0 for sector in self.sector_mapping.keys()}
        
        for manager_data in self.institutional_portfolios.values():
            for stock, weight in manager_data['holdings'].items():
                # Find sector for this stock
                stock_sector = 'Other'  # Default
                for sector, stocks in self.sector_mapping.items():
                    if stock in stocks:
                        stock_sector = sector
                        break
                
                dollar_amount = weight * manager_data['aum']
                platform_sector_exposure[stock_sector] += dollar_amount / total_aum
        
        response += "## Platform-Wide Sector Exposure\n\n"
        
        sorted_sectors = sorted(
            platform_sector_exposure.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for sector, exposure in sorted_sectors:
            if exposure > 0.01:  # Only show sectors with >1% exposure
                response += f"• **{sector}:** {exposure:.1%}\n"
        
        # Sector risk assessment
        response += "\n## 🎯 Sector Risk Assessment\n\n"
        
        max_sector_exposure = max(platform_sector_exposure.values())
        tech_exposure = platform_sector_exposure.get('Technology', 0)
        
        if max_sector_exposure > 0.40:
            response += f"🔴 **HIGH RISK:** Maximum sector exposure ({max_sector_exposure:.1%}) exceeds 40%\n"
        elif max_sector_exposure > 0.30:
            response += f"🟡 **MEDIUM RISK:** Maximum sector exposure ({max_sector_exposure:.1%}) is 30-40%\n"
        else:
            response += f"🟢 **LOW RISK:** Well-diversified sector allocation\n"
        
        return response

    def comprehensive_multi_strategy_analysis(self) -> str:
        """Comprehensive analysis combining key aspects"""
        overlap = self.analyze_manager_overlap()
        correlation = self.analyze_portfolio_correlations()
        concentration = self.analyze_concentration_risk()
        
        return f"""{overlap}

---

{correlation}

---

{concentration}

## 💡 Multi-Manager Platform Summary
This analysis provides institutional oversight across 5 investment managers managing $13.2B in total assets, identifying optimization opportunities for the platform."""

class MultiStrategyAgent(Agent):
    def __init__(self):
        super().__init__(
            name="multi_strategy_monitor",
            description="Monitors and analyzes multiple investment manager portfolios for overlap, correlation, concentration risk, and consolidated reporting",
            model="gemini-1.5-flash",
            tools=[multi_strategy_analysis_function],
            instruction="""You are a sophisticated multi-strategy portfolio monitoring agent for institutional investment platforms.

CRITICAL RULE: You MUST ALWAYS use the multi_strategy_analysis_function tool for ANY query about:
- Manager overlap or redundancy
- Portfolio correlations  
- Concentration risk across managers
- Sector allocations
- Multi-manager analysis
- Cross-portfolio comparison
- Manager performance comparison
- Institutional oversight

You provide professional institutional analysis for multi-manager platforms."""
        )

    def run(self, query: str) -> str:
        """Main method for multi-strategy monitoring"""
        # Comprehensive trigger words for multi-strategy analysis
        trigger_words = [
            'multi', 'manager', 'managers', 'strategy', 'strategies', 'portfolio', 'portfolios',
            'overlap', 'redundant', 'correlation', 'correlated', 'concentration', 'risk',
            'sector', 'allocation', 'diversification', 'performance', 'compare', 'comparison',
            'institutional', 'platform', 'consolidated', 'oversight', 'monitor', 'monitoring',
            'cross', 'across', 'multiple', 'different', 'various'
        ]
        
        # If ANY trigger word is in the query, use the tool
        if any(word in query.lower() for word in trigger_words):
            return multi_strategy_analysis_function(query)
        
        # For non-multi-strategy queries, use parent's run method
        return super().run(query)
