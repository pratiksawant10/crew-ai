# trip_planner_crew.py
import os
from crewai import Agent, Task, Crew
from crewai_tools import Tool
from textwrap import dedent
from dotenv import load_dotenv
from tools.search_tools import SearchTools as tools # Import the tools

# Load environment variables for API keys
load_dotenv()

class TripCrew:
    """
    A CrewAI project to plan an ideal trip based on user inputs.
    """
    def __init__(self, location, cities, date_range, interests):
        self.location = location
        self.cities = cities
        self.date_range = date_range
        self.interests = interests
        
    def get_tools(self):
        """Returns the list of tools available to the agents."""
        return tools

    ## Agents Definition (from your prompt)
    # ------------------------------------
    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city from the options based on weather, season, and prices, and justify the choice.',
            backstory='An expert in analyzing travel data to pick ideal destinations, known for finding hidden gems that match traveler interests.',
            tools=self.get_tools(),
            verbose=True
        )

    def local_expert(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city, including top 5 must-see attractions, local customs, and seasonal advice.',
            backstory="""A knowledgeable local guide with extensive information
            about the city, its attractions, and customs. Known for insider tips.""",
            tools=self.get_tools(),
            verbose=True
        )

    def travel_concierge(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing 3-day travel itinerary with a daily budget, 
            packing suggestions, and a final summary of the whole plan.""",
            backstory="""Specialist in travel planning and logistics with 
            decades of experience, creating personalized, detailed, and realistic plans.""",
            tools=self.get_tools(),
            verbose=True
        )
    # ------------------------------------


    ## Tasks Definition
    # ------------------------------------
    def city_selection_task(self):
        return Task(
            description=dedent(f"""
                Analyze the following city options: {self.cities}.
                Consider the travel date range: {self.date_range}.
                Analyze weather, seasonal events, and general price levels for each city.
                Select ONE city that is the best fit for these constraints and the user's
                high-level interests: {self.interests}.
                The final output MUST be the name of the selected city and a brief (3-5 sentence)
                justification for the choice.
            """),
            agent=self.city_selection_agent(),
            expected_output='A single city name and a justification.',
        )

    def local_expert_task(self):
        return Task(
            description=dedent(f"""
                Using the city selected in the previous task, provide a comprehensive
                local report. The user is traveling from {self.location}.
                Your report must include:
                1. Top 5 must-see attractions or experiences.
                2. 3 crucial local customs or etiquette tips.
                3. Specific seasonal advice for the travel date range: {self.date_range}.
                4. Suggestions tailored to the user's interests: {self.interests}.
            """),
            agent=self.local_expert(),
            context=[self.city_selection_task()], # Use the output of the first task
            expected_output='A detailed report covering the 4 required points.',
        )
    
    def travel_concierge_task(self):
        return Task(
            description=dedent(f"""
                Based on the city selection and the local expert's report, create a
                detailed 3-day travel itinerary. The user is traveling from {self.location}
                in the date range of {self.date_range}.
                
                Your itinerary must include:
                1. A daily schedule (Morning, Afternoon, Evening) for 3 days.
                2. A realistic daily budget (estimate).
                3. A final section on **packing suggestions** considering the weather and local customs.
                4. A final summary of the entire trip plan.
            """),
            agent=self.travel_concierge(),
            context=[self.local_expert_task()], # Use the output of the second task
            expected_output='A complete, structured 3-day itinerary with budget, packing tips, and a summary.',
        )
    # ------------------------------------

    def run(self):
        """Orchestrates the agents and tasks into a sequential crew."""
        print("\n--- CREW INITIALIZED ---\n")
        
        # 1. Instantiate the tasks
        task_city = self.city_selection_task()
        task_local = self.local_expert_task()
        task_concierge = self.travel_concierge_task()
        
        # 2. Instantiate the crew
        trip_crew = Crew(
            agents=[
                self.city_selection_agent(),
                self.local_expert(),
                self.travel_concierge()
            ],
            tasks=[
                task_city,
                task_local,
                task_concierge
            ],
            # Sequential execution is perfect for this flow
            # The output of one task feeds into the next
            process='sequential' 
        )

        # 3. Kick off the crew
        print("Starting Trip Planner Crew...")
        result = trip_crew.kickoff()
        print("\n--- CREW COMPLETE ---")
        return result


if __name__ == "__main__":
    # The interactive input logic
    print("## Welcome to Trip Planner Crew")
    print('-------------------------------')
    
    # You need to configure your environment variables for the LLM to work.
    # e.g., OPENAI_API_KEY, GROQ_API_KEY, etc.
    if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("GROQ_API_KEY"):
        print("\n**WARNING**: Please set your LLM API Key (e.g., OPENAI_API_KEY) in your .env file to run the crew.")
        # Provide placeholder values for the structure to work
        # In a real scenario, this would block execution.
        print("Using placeholder inputs for demonstration.")
        
    location = input(dedent("From where will you be traveling from? "))
    cities = input(dedent("What are the cities options you are interested in visiting (e.g., Paris, Tokyo, Sydney)? "))
    date_range = input(dedent("What is the date range you are interested in traveling (e.g., Dec 15 - Dec 22)? "))
    interests = input(dedent("What are some of your high level interests and hobbies (e.g., history, food, hiking)? "))

    # Run the crew
    trip_planner_crew = TripCrew(location, cities, date_range, interests)
    result = trip_planner_crew.run()
    
    print("\n\n########################")
    print("## FINAL TRIP PLAN REPORT ##")
    print("########################\n")
    print(result)