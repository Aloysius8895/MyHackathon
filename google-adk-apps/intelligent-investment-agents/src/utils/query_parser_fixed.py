# src/utils/query_parser_fixed.py - Fixed with between pattern
import re
from typing import Dict, List, Any

class QueryParser:
    """Parse natural language investment queries into screening criteria"""
    
    def __init__(self):
        self.criteria_patterns = {
            'dividend': r'dividend|yield|income',
            'growth': r'growth|growing|expanding',
            'value': r'value|cheap|undervalued',
            'large_cap': r'large cap|big|established|blue chip',
            'tech': r'tech|technology|software|ai|artificial intelligence',
            'financial': r'bank|financial|finance|insurance',
            'healthcare': r'health|pharma|medical|biotech',
            'energy': r'energy|oil|gas|renewable',
            'price_under': r'price under \$?(\d+)|under \$(\d+)|below \$(\d+)|less than \$(\d+)',
            'price_over': r'price over \$?(\d+)|over \$(\d+)|above \$(\d+)|more than \$(\d+)',
            'price_between': r'between \$?(\d+) and \$?(\d+)',
            'pe_under': r'pe under (\d+)|p/e under (\d+)|pe below (\d+)|p/e below (\d+)',
            'yield_over': r'yield over (\d+)|yield above (\d+)|dividend over (\d+)'
        }
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query into structured criteria"""
        query_lower = query.lower()
        criteria = {}
        
        for criterion, pattern in self.criteria_patterns.items():
            if re.search(pattern, query_lower):
                if criterion == 'price_under':
                    match = re.search(pattern, query_lower)
                    if match:
                        price = next((group for group in match.groups() if group), None)
                        criteria['max_price'] = float(price) if price else None
                elif criterion == 'price_over':
                    match = re.search(pattern, query_lower)
                    if match:
                        price = next((group for group in match.groups() if group), None)
                        criteria['min_price'] = float(price) if price else None
                elif criterion == 'price_between':
                    match = re.search(pattern, query_lower)
                    if match:
                        min_price = match.group(1)
                        max_price = match.group(2)
                        criteria['min_price'] = float(min_price) if min_price else None
                        criteria['max_price'] = float(max_price) if max_price else None
                elif criterion == 'pe_under':
                    match = re.search(pattern, query_lower)
                    if match:
                        pe = next((group for group in match.groups() if group), None)
                        criteria['max_pe'] = float(pe) if pe else None
                elif criterion == 'yield_over':
                    match = re.search(pattern, query_lower)
                    if match:
                        yield_val = next((group for group in match.groups() if group), None)
                        criteria['min_dividend_yield'] = float(yield_val) if yield_val else None
                else:
                    criteria[criterion] = True
        
        criteria['original_query'] = query
        return criteria
    
    def apply_filters(self, stocks: List[Dict], criteria: Dict) -> List[Dict]:
        """Apply parsed criteria to filter stock list"""
        filtered_stocks = []
        
        for stock in stocks:
            include_stock = True
            
            if criteria.get('max_price') and stock.get('price'):
                if stock['price'] > criteria['max_price']:
                    include_stock = False
            
            if criteria.get('min_price') and stock.get('price'):
                if stock['price'] < criteria['min_price']:
                    include_stock = False
            
            if criteria.get('max_pe') and stock.get('pe_ratio'):
                if stock['pe_ratio'] > criteria['max_pe']:
                    include_stock = False
            
            if criteria.get('min_dividend_yield') and stock.get('dividend_yield'):
                if stock['dividend_yield'] < criteria['min_dividend_yield']:
                    include_stock = False
            
            if criteria.get('dividend'):
                if not stock.get('dividend_yield') or stock['dividend_yield'] < 1:
                    include_stock = False
            
            sector = stock.get('sector', '').lower()
            if criteria.get('tech') and 'technology' not in sector:
                include_stock = False
            if criteria.get('financial') and 'financial' not in sector:
                include_stock = False
            if criteria.get('healthcare') and 'healthcare' not in sector:
                include_stock = False
            
            if include_stock:
                filtered_stocks.append(stock)
        
        return filtered_stocks
