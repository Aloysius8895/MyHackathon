import yfinance as yf
from datetime import datetime

region_suffix = {
    "USA": "",
    "India": ".NS",
    "UK": ".L",
    "Germany": ".DE",
    "Japan": ".T"
}

class DataAgent:
    def get_real_time_data(self, ticker: str, region: str) -> dict:
        suffix = region_suffix.get(region, "")
        full_ticker = f"{ticker}{suffix}"
        stock = yf.Ticker(full_ticker)
        info = stock.info

        return {
            "price": info.get("currentPrice", info.get("regularMarketPrice")),
            "currency": info.get("currency"),
            "updated_at": datetime.now().isoformat(),
            "volume": info.get("regularMarketVolume")
        }