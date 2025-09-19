import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))

root_agent = Agent(
    model=os.getenv("DEFAULT_MODEL"),
    name='search_agent',
    description="Search agent with Google search capabilities",
    instruction="""You are a helpful assistant that can use the following tools:
    - google_search: Search the web for current information
    """,
    tools=[google_search],
)
