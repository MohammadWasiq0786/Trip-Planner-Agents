from crewai import Agent, Task, Crew
from euriai import EuriaiClient

# Initialize the API client with your API key and model
EURIAI_API_KEY = "API_KEY"  # Replace with your actual API key

# Initialize the client
client = EuriaiClient(
    api_key=EURIAI_API_KEY,  # Replace with your actual API key
    model="gpt-4.1-nano",
)


class TripAgents:
    def __init__(self):
        self.client = client

    def generate_agent_response(self, role, goal, backstory, verbose=True):
        prompt = (
            f"Role: {role}\n"
            f"Goal: {goal}\n"
            f"Backstory: {backstory}\n"
            "Please act as an expert in this role and provide detailed, helpful responses."
        )
        # Call with prompt as positional argument
        response = self.client.generate_completion(
            prompt, temperature=0.7, max_tokens=500
        )
        return response["choices"][0]["message"][
            "content"
        ]  # if verbose else response['choices'][0]['message']['content'].strip()

    def city_selector_agent(self):
        return self.generate_agent_response(
            role="City Selection Expert",
            goal="Identify best cities to visit based on user preferences",
            backstory=(
                "An expert travel geographer with extensive knowledge about world cities "
                "and their cultural, historical, and entertainment offerings"
            ),
            verbose=True,
        )

    def local_expert_agent(self):
        return self.generate_agent_response(
            role="Local Destination Expert",
            goal="Provide detailed insights about selected cities including top attractions, local customs, and hidden gems",
            backstory="A knowledgeable local guide with first-hand experience of the city's culture and attractions",
            verbose=True,
        )

    def travel_planner_agent(self):
        return self.generate_agent_response(
            role="Professional Travel Planner",
            goal="Create detailed day-by-day itineraries with time allocations, transportation options, and activity sequencing",
            backstory="An experienced travel coordinator with perfect logistical planning skills",
            verbose=True,
        )

    def budget_manager_agent(self):
        return self.generate_agent_response(
            role="Travel Budget Specialist",
            goal="Optimize travel plans to stay within budget while maximizing experience quality",
            backstory="A financial planner specializing in travel budgets and cost optimization",
            verbose=True,
        )


class TripTasks:
    def __init__(self):
        self.client = client

    def city_selection_task(self, inputs):
        description = (
            f"Analyze user preferences and select the best destinations:\n"
            f"- Travel Type: {inputs['travel_type']}\n"
            f"- Interests: {inputs['interests']}\n"
            f"- Season: {inputs['season']}\n"
            "Output: Provide 3 city options with a brief rationale for each."
        )
        # Call with prompt as positional argument
        response = self.client.generate_completion(
            description, temperature=0.7, max_tokens=300
        )

        return response["choices"][0]["message"][
            "content"
        ]  # if verbose else response['choices'][0]['message']['content'].strip()

    def city_research_task(self, city):
        description = (
            f"Provide detailed insights about {city} including:\n"
            "- Top 5 attractions\n"
            "- Local cuisine highlights\n"
            "- Cultural norms/etiquette\n"
            "- Recommended accommodation areas\n"
            "- Transportation tips"
        )
        response = self.client.generate_completion(
            description, temperature=0.7, max_tokens=500
        )

        return response["choices"][0]["message"][
            "content"
        ]  # if verbose else response['choices'][0]['message']['content'].strip()

    def itinerary_creation_task(self, inputs, city):
        description = (
            f"Create a {inputs['duration']}-day itinerary for {city} including:\n"
            "- Daily schedule with time allocations\n"
            "- Activity sequencing\n"
            "- Transportation between locations\n"
            "- Meal planning suggestions"
        )
        response = self.client.generate_completion(
            description, temperature=0.7, max_tokens=600
        )

        return response["choices"][0]["message"][
            "content"
        ]  # if verbose else response['choices'][0]['message']['content'].strip()

    def budget_planning_task(self, inputs, itinerary):
        description = (
            f"Create a budget plan for the trip with a total budget of {inputs['budget']} covering:\n"
            "- Accommodation costs\n"
            "- Transportation expenses\n"
            "- Activity fees\n"
            "- Meal budget\n"
            "- Emergency funds allocation\n"
            f"Based on the itinerary: {itinerary}"
        )
        response = self.client.generate_completion(
            description, temperature=0.7, max_tokens=500
        )

        return response["choices"][0]["message"][
            "content"
        ]  # if verbose else response['choices'][0]['message']['content'].strip()


class TripCrew:
    def __init__(self, inputs):
        self.inputs = inputs
        self.agents = TripAgents()
        self.tasks = TripTasks()

    def run(self):
        # Generate responses for each role
        city_selector_response = self.agents.city_selector_agent()
        local_expert_response = self.agents.local_expert_agent()
        travel_planner_response = self.agents.travel_planner_agent()
        budget_manager_response = self.agents.budget_manager_agent()

        # For demonstration, assume the city selected is "Paris"
        city = "Paris"

        # Run tasks
        city_research_response = self.tasks.city_research_task(city)
        itinerary_response = self.tasks.itinerary_creation_task(self.inputs, city)
        budget_response = self.tasks.budget_planning_task(
            self.inputs, itinerary_response
        )

        # Collect all responses
        final_result = {
            "city_selection": city_selector_response,
            "city_research": city_research_response,
            "itinerary": itinerary_response,
            "budget": budget_response,
        }

        # Print responses for debugging
        print("City Selector Response:", city_selector_response)
        print("City Research Response:", city_research_response)
        print("Itinerary Response:", itinerary_response)
        print("Budget Response:", budget_response)

        return final_result
