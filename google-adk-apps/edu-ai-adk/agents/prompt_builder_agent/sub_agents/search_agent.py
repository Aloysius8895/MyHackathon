from google.adk.agents import Agent
from google.adk.tools import google_search

search_agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    description="Searches for data and quotes on ENEM topics using Google Search",
    tools=[google_search],
    instruction="""
You are a specialist in information retrieval.

Upon receiving a thematic area, use the google_search tool to gather:

- statistical data
- expert quotes
- historical facts

Based on these, generate and return 3 different short texts, each with data, quotes, and context about the topic. Do not invent facts.
"""
)
