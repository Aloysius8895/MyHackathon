# technical_agent.py - Analyzes stock trends

import pandas as pd
from datetime import datetime

class TechnicalAnalysisAgent:
    """This agent analyzes stock trends and gives buy/sell signals"""
    
    def __init__(self):
        self.name = "Technical Analysis Agent"
        self.price_history = {}  # Stores price history for each stock
    
    def add_price_data(self, symbol, price):
        """Add new price data for a stock"""
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        self.price_history[symbol].append({
            "price": price,
            "timestamp": datetime.now()
        })
        
        # Keep only last 20 prices (for analysis)
        if len(self.price_history[symbol]) > 20:
            self.price_history[symbol] = self.price_history[symbol][-20:]
    
    def calculate_moving_average(self, symbol, periods=5):
        """Calculate average price over last few periods"""
        if symbol not in self.price_history:
            return None
        
        prices = [item["price"] for item in self.price_history[symbol]]
        if len(prices) < periods:
            return None
        
        recent_prices = prices[-periods:]
        return sum(recent_prices) / len(recent_prices)
    
    def generate_signal(self, symbol, current_price):
        """Generate buy/sell/hold signal"""
        # Calculate moving averages
        short_ma = self.calculate_moving_average(symbol, 5)  # 5-period average
        long_ma = self.calculate_moving_average(symbol, 10)  # 10-period average
        
        if not short_ma or not long_ma:
            return "HOLD", "Not enough data"
        
        # Simple trading logic
        if current_price > short_ma > long_ma:
            return "BUY", f"Price ${current_price} above averages (${short_ma:.2f}, ${long_ma:.2f})"
        elif current_price < short_ma < long_ma:
            return "SELL", f"Price ${current_price} below averages (${short_ma:.2f}, ${long_ma:.2f})"
        else:
            return "HOLD", f"Mixed signals - Price: ${current_price}, Averages: ${short_ma:.2f}, ${long_ma:.2f}"
    
    def analyze_stock(self, symbol, price):
        """Analyze a single stock"""
        # Add price to history
        self.add_price_data(symbol, price)
        
        # Generate signal
        signal, reason = self.generate_signal(symbol, price)
        
        return {
            "symbol": symbol,
            "price": price,
            "signal": signal,
            "reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Test the technical agent
if __name__ == "__main__":
    tech_agent = TechnicalAnalysisAgent()
    
    # Simulate some price data
    test_prices = [150, 152, 148, 155, 160, 158, 162, 165, 163, 168]
    
    print(f"🤖 Testing {tech_agent.name}...")
    
    for i, price in enumerate(test_prices):
        result = tech_agent.analyze_stock("AAPL", price)
        print(f"Day {i+1}: {result['signal']} - {result['reason']}")