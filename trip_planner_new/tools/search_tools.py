# tools/search_tools.py
import json
import os
from dotenv import load_dotenv
from crewai_tools import Tool

load_dotenv()

# Example Tool - uses the Google Search API behind the scenes
# In a real CrewAI project, you'd configure a specific search tool,
# but for this example, we'll use a placeholder that suggests a search.
def google_search(query):
    """
    Simulates a real-time Google search for up-to-date travel information.
    In a complete CrewAI setup, you would replace this with an actual
    tool that calls a search API (e.g., using `crewai_tools.GoogleSearchTool`).
    """
    print(f"--- TOOL EXECUTED: Google Search for '{query}' ---")
    # Placeholder return:
    return f"Search results for '{query}' weather, seasonal info, and budget."

# Define the set of tools for the agents
SearchTools = [
    Tool(
        name="Internet Search",
        func=google_search,
        description="A powerful tool for searching the internet for real-time data, including weather, prices, seasonal events, and local customs."
    )
]