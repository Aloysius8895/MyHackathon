from dotenv import load_dotenv

load_dotenv()
from agents import NewsAgent, TrendsAgent, DataAgent, InsightsAgent, PortfolioAdvisor


class StockOrchestrator:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.trends_agent = TrendsAgent()
        self.data_agent = DataAgent()
        self.insights_agent = InsightsAgent()
        self.portfolio_advisor = PortfolioAdvisor()

    def full_analysis(self, ticker: str, risk_profile: str, region: str) -> dict:
        news_summary = self.news_agent.get_news_summary(ticker, region)  # Update if region-specific later
        trends = self.trends_agent.analyze(ticker, region)
        real_time_data = self.data_agent.get_real_time_data(ticker, region)
        ai_insights = self.insights_agent.generate_advice(news_summary, trends)
        portfolio = self.portfolio_advisor.recommend_allocation(risk_profile, ai_insights)

        return {
            "real_time_data": real_time_data,
            "news_summary": news_summary,
            "technical_analysis": trends,
            "ai_insights": ai_insights,
            "portfolio_recommendation": portfolio
        }