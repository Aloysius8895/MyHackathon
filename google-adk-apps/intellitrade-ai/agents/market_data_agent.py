# market_data_agent.py - Your first AI agent!

import yfinance as yf  # Gets stock prices
import time
import json
from datetime import datetime

class MarketDataAgent:
    """This agent collects stock market data"""
    
    def __init__(self):
        self.name = "Market Data Agent"
        self.stocks = ["AAPL", "MSFT", "GOOGL", "TSLA"]  # Stocks to watch
        
    def get_stock_price(self, symbol):
        """Get current price for a stock"""
        try:
            # Download stock data
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d", interval="1m")
            
            if not data.empty:
                latest_price = data['Close'].iloc[-1]
                return {
                    "symbol": symbol,
                    "price": round(float(latest_price), 2),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            print(f"Error getting price for {symbol}: {e}")
            return None
    
    def collect_all_data(self):
        """Collect data for all stocks"""
        print(f"🤖 {self.name} is collecting market data...")
        
        all_data = []
        for stock in self.stocks:
            price_data = self.get_stock_price(stock)
            if price_data:
                all_data.append(price_data)
                print(f"📈 {stock}: ${price_data['price']}")
        
        return all_data
    
    def run_forever(self):
        """Keep collecting data every minute"""
        print(f"🚀 Starting {self.name}...")
        
        while True:
            try:
                data = self.collect_all_data()
                print(f"✅ Collected data for {len(data)} stocks")
                print("-" * 50)
                
                # Wait 1 minute before next collection
                time.sleep(60)
                
            except KeyboardInterrupt:
                print(f"🛑 {self.name} stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(10)  # Wait 10 seconds before retrying

# Test the agent
if __name__ == "__main__":
    agent = MarketDataAgent()
    agent.run_forever()