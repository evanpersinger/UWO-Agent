# agent.py
# This agent helps students research courses at Western University.

from agentic.common import Agent, AgentRunner 
from agentic.models import GPT_4O_MINI
from agentic.tools import  OpenAIWebSearchTool
from dotenv import load_dotenv
from openai import OpenAI
import os
from urllib.request import urlopen
from urllib.error import URLError


load_dotenv()  # This loads variables from .env into os.environ

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# URLs that the agent can access
# websites the agent uses to answer questions.
COURSE_URLS = [
    "https://westerncalendar.uwo.ca/Courses.cfm",
    "https://westerncalendar.uwo.ca/SessionalDates.cfm?SelectedCalendar=Live&ArchiveID=",
]



# fetch content from a URL
def fetch_url(url: str) -> str:
    """Fetches and returns the content from a specific URL."""
    try:
        with urlopen(url) as response:
            content = response.read().decode('utf-8')
            return content
    except URLError as e:
        return f"Could not fetch {url}: {e}"
    except Exception as e:
        return f"Error fetching {url}: {e}"



Model=GPT_4O_MINI


# agent
agent = Agent(
    name="UWO Agent", # agent's name
    model=Model, # model the agent will use
    
    # how the ai agent functions
    instructions="""
    
    You're a helpful assistant that helps students research courses at Western University.
    You will also help answer any questions students have regarding the courses at Western University.
    You have access to a lot of information about the courses at Western University.
    
    
    ### Student Questions
    Students will commonly ask you questions about:
    Course prerequisites, co-requisites, and antirequisites.
    Course descriptions. 
    Course syllabus information.
    
    
    """,
    
    
    
 
    
    
    # tools ai agent has access to
    tools=
    [
    fetch_url,
    OpenAIWebSearchTool()
    ], 
)



# Launch the REPL loop
if __name__ == "__main__":
    AgentRunner(agent).repl_loop()





