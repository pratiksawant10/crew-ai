from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

class TripAgents():
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7
        )
        try:
            self.search = DuckDuckGoSearchRun()
        except ImportError:
            print("Warning: DuckDuckGo search not available. Using basic fallback.")
            
            class DummySearch:
                def run(self, query):
                    return "Search functionality unavailable"
            
            self.search = DummySearch()

    def get_tools(self):
    return [
        {
            "name": "Search",
            "description": "Useful for searching information on the internet",
            "func": self.search.run
        }
    ]

    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=self.get_tools(),
            llm=self.llm,
            verbose=True
        )

    def local_expert(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information
            about the city, its attractions and customs""",
            tools=self.get_tools(),
            llm=self.llm,
            verbose=True
        )

    def travel_concierge(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
            decades of experience""",
            tools=self.get_tools(),
            llm=self.llm,
            verbose=True
        )
