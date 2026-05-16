import pytest
from agents import NewsAgent, TrendsAgent, DataAgent
from unittest.mock import patch

@pytest.fixture
def sample_ticker():
    return "AAPL"

def test_news_agent_fetch(sample_ticker):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'articles': [{'url': 'http://test.com'}]}
        news = NewsAgent().get_news_summary(sample_ticker)
        assert isinstance(news, str)

def test_trends_analysis(sample_ticker):
    agent = TrendsAgent()
    analysis = agent.analyze(sample_ticker)
    assert 'moving_averages' in analysis
    assert 7 in analysis['moving_averages']

def test_data_agent_real_time(sample_ticker):
    data = DataAgent().get_real_time_data(sample_ticker)
    assert isinstance(data['price'], float)
    assert data['currency'] == 'USD'
