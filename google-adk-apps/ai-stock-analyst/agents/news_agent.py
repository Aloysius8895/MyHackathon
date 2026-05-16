from newsapi import NewsApiClient
import os

class NewsAgent:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.newsapi = NewsApiClient(api_key=self.api_key)

    def get_news_summary(self, ticker: str, region: str) -> list:
        try:
            search_term = f"{ticker} stock {region}"
            articles = self.newsapi.get_everything(
                q=search_term,
                language='en',
                sort_by='publishedAt',
                page_size=3
            )

            if not articles['articles']:
                return []

            summary_list = []
            for article in articles['articles']:
                summary_list.append({
                    "title": article.get("title", "No Title"),
                    "summary": article.get("description", "No summary available."),
                    "link": article.get("url", "")
                })

            return summary_list

        except Exception as e:
            return [{
                "title": "News Fetch Error",
                "summary": str(e),
                "link": ""
            }]