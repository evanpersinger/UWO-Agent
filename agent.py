# agent.py
# This agent helps students research courses at Western University.
# This agent requires the use of an openai api key in order to function.

from agents import Agent, Runner, function_tool, WebSearchTool
from dotenv import load_dotenv
import os
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
from functools import lru_cache


load_dotenv()  # This loads variables from .env into os.environ

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# URLs that the agent can access
# websites the agent uses to answer questions.
COURSE_URLS = [
    "https://westerncalendar.uwo.ca/Courses.cfm",
    "https://westerncalendar.uwo.ca/SessionalDates.cfm?SelectedCalendar=Live&ArchiveID=",
]


# fetch content from a URL (internal, cached).
# used directly by the helpers below AND wrapped as the fetch_url tool, so it
# stays a plain function that we can call from Python.
@lru_cache(maxsize=50)
def _fetch_url(url: str) -> str:
    """Fetches and returns the parsed text content from a specific URL. Results are cached."""
    try:
        with urlopen(url) as response:
            html_content = response.read().decode('utf-8')
            # Parse HTML and extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            # Get text and clean it up
            text = soup.get_text(separator=' ', strip=True)
            return text
    except URLError as e:
        return f"Could not fetch {url}: {e}"
    except Exception as e:
        return f"Error fetching {url}: {e}"


# Load user profile safely
def _load_user_profile() -> str:
    """returns empty string if file doesn't exist or is empty."""
    profile_path = os.path.join(BASE_DIR, "user_profile.md")
    if not os.path.exists(profile_path):
        return "User profile not found. Please fill in user_profile.md for personalized advice."
    try:
        with open(profile_path, 'r') as f:
            content = f.read().strip()
            if not content or content.startswith("# User's profile"):
                return "User profile is empty. Please fill in user_profile.md with your campus, program, year, and completed courses for personalized advice."
            return content
    except Exception as e:
        return f"Error loading user profile: {e}"


# ---- Tools the agent can call ----

@function_tool
def fetch_url(url: str) -> str:
    """Fetches and returns the parsed text content from a specific URL. Results are cached."""
    return _fetch_url(url)


@function_tool
def check_prerequisites(course_code: str) -> str:
    """
    Checks if the user has completed prerequisites for a given course.
    Returns information about missing prerequisites based on user profile.

    Args:
        course_code: Course code ("CS1027", "MATH1600")
    """
    user_profile = _load_user_profile()
    if "User profile" in user_profile and "courses:" in user_profile.lower():
        # Extract completed courses from profile
        completed_courses = []
        for line in user_profile.split('\n'):
            if re.match(r'^[A-Z]{2,4}\s?\d{4}', line.strip(), re.IGNORECASE):
                completed_courses.append(line.strip().upper())

        # Fetch course info to check prerequisites
        course_url = f"https://westerncalendar.uwo.ca/Courses.cfm?SelectedCalendar=Live&ArchiveID="
        course_info = _fetch_url(course_url)

        # Look for course in the fetched data
        course_code_upper = course_code.upper().replace(' ', '')
        if course_code_upper in course_info:
            return f"Found course {course_code}. Use fetch_url to get detailed prerequisite information, then compare with user's completed courses: {', '.join(completed_courses) if completed_courses else 'None listed'}."
        else:
            return f"Course {course_code} not found in main catalog. It may be at an affiliate college. User's completed courses: {', '.join(completed_courses) if completed_courses else 'None listed'}."
    else:
        return "User profile not loaded. Cannot check prerequisites. Please fill in user_profile.md with completed courses."


@function_tool
def search_courses(query: str) -> str:
    """
    Searches for courses by name or code.

    Args:
        query: Search term (course name, code, or keywords)
    """
    course_url = COURSE_URLS[0]
    course_data = _fetch_url(course_url)

    # Simple search in the course data
    query_lower = query.lower()
    matches = []
    lines = course_data.split('\n')

    for i, line in enumerate(lines):
        if query_lower in line.lower():
            # Get context around the match
            context = ' '.join(lines[max(0, i-1):min(len(lines), i+2)])
            matches.append(context)
            if len(matches) >= 10:  # Limit results
                break

    if matches:
        return f"Found {len(matches)} potential matches for '{query}':\n\n" + "\n\n---\n\n".join(matches[:5])
    else:
        return f"No courses found matching '{query}'. Try a different search term or check affiliate college catalogs."


@function_tool
def get_completed_courses() -> str:
    """Returns a list of courses the user has completed from their profile."""
    user_profile = _load_user_profile()
    if "courses:" in user_profile.lower():
        courses = []
        in_courses_section = False
        for line in user_profile.split('\n'):
            if 'courses:' in line.lower():
                in_courses_section = True
                continue
            if in_courses_section and line.strip():
                courses.append(line.strip())

        if courses:
            return f"Completed courses: {', '.join(courses)}"

    return "No completed courses found in user profile. Please add them to user_profile.md"


# model used by the agent
MODEL = "gpt-4o-mini"


# how the ai agent functions. The student's profile is folded in at the end so
# the agent can give personalized advice (the OpenAI Agents SDK has no separate
# "memories" concept, so this lives in the instructions).
INSTRUCTIONS = f"""

You're an expert in course planning and scheduling at Western University.
You're a helpful assistant that helps students research courses at Western University.
You will also help answer any questions students have regarding courses at Western University.
Use the given links to find information about the courses at Western University.


### Student Questions
Students will commonly ask you questions about:
Course prerequisites, co-requisites, and antirequisites.
Course descriptions.
Course syllabus information.
Course recommendations based on their program and completed courses.
Whether they can take a specific course (prerequisite checking).
If you don't understand a student's question, ask them to clarify.


### Core Requisites and Scheduling Conflicts
Important: Sometimes a "co-requisite" (courses that must be taken at the same time) can effectively function as a prerequisite if the courses don't occur at the same time due to scheduling conflicts.
In such cases, students may need to complete the corequisite course first before taking the other course. When advising students about course planning,
consider this scenario and help them understand that they may need to take corequisite courses in sequence rather than simultaneously if scheduling doesn't allow for concurrent enrollment.


### Available Tools
- Use `search_courses(query)` to find courses by name or code
- Use `check_prerequisites(course_code)` to verify if the student has met prerequisites
- Use `get_completed_courses()` to see what courses the student has already taken
- Use `fetch_url(url)` to get detailed course information from the calendar

### Things to consider when answering questions
- Sometimes a course is only offered at an affiliate college, so you need to check the course catalog of the affiliate college to see if the course is offered.
- When recommending courses, consider the student's program, year, and completed courses from their profile.
- Always check prerequisites before recommending a course.

### Student Profile
The following is the student's profile. Use it to personalize your answers:
{_load_user_profile()}

"""


# agent
agent = Agent(
    name="UWO Agent",          # agent's name
    model=MODEL,               # model the agent will use
    instructions=INSTRUCTIONS,  # how the ai agent functions
    # tools ai agent has access to
    tools=[
        fetch_url,
        WebSearchTool(),
        check_prerequisites,
        search_courses,
        get_completed_courses,
    ],
)


# Launch the REPL loop
if __name__ == "__main__":
    print("UWO Course Research Agent. Ask about Western courses. Type 'exit' to quit.")
    conversation = []
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue
        conversation.append({"role": "user", "content": user_input})
        result = Runner.run_sync(agent, conversation)
        print(result.final_output)
        conversation = result.to_input_list()
