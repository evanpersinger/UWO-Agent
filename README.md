# UWO Course Research Agent

An AI agent that helps students research and plan courses at Western University. The agent is an expert in course planning and scheduling, and can answer questions about course prerequisites, descriptions, syllabi, and provide personalized course recommendations.

## Features

- Answer questions about Western University courses
- Access course information from the Western University calendar
- Search for courses by name or code
- Check if you've met prerequisites for specific courses
- Get personalized course recommendations based on your program and completed courses
- View your completed course history
- Help with prerequisites, co-requisites, and antirequisites
- Provide course descriptions and syllabus information
- Cached course data for faster responses

## Prerequisites

Before installing, make sure you have the following:

- **Python 3.x** - Check with: `python --version` or `python3 --version`
- **pip** - Python package manager (usually comes with Python). Check with: `pip --version` or `pip3 --version`
- **Git** - For cloning the repository. Check with: `git --version`
- **OpenAI API Key** - Required for the agent to function. Get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

If any of these are missing, install them before proceeding with the installation.

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd uwo_course_repo
```

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv venv
```

Then activate it:
- On macOS/Linux: `source venv/bin/activate`
- On Windows: `venv\Scripts\activate`

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

**Important:** The agent requires an OpenAI API key to function. Without it, the agent will not work.

1. Create a `.env` file in the project root
2. Add your OpenAI API key (get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)):

```
OPENAI_API_KEY=your_api_key_here
```

3. Fill in your student profile in `user_profile.md` with your information (e.g., your program, year, courses you've taken, etc.) so the agent can provide personalized advice.

## Usage

1. Make sure you've completed the Setup steps above (created `.env` file and filled in `user_profile.md`)

2. If you're using a virtual environment, activate it:
   - On macOS/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

3. Run the agent:

```bash
python agent.py
```

The agent will start a REPL loop where you can ask questions about Western University courses. Type your questions and the agent will help you find the information you need.

### Example Questions

- "Can I take CS1027?" - Checks if you've met the prerequisites
- "Search for psychology courses" - Finds courses matching your search
- "What courses have I completed?" - Shows your course history
- "Recommend courses for my program" - Gets personalized recommendations
- "What are the prerequisites for MATH1000?" - Gets prerequisite information

To exit the agent, type `exit` or press `Ctrl+C`.

## Project Structure

- `agent.py` - Main agent implementation
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file with your API key)
- `user_profile.md` - Student profile information (fill this in during setup)

## Tools

The agent has access to:
- `fetch_url` - Fetches content from Western University course calendar URLs (with caching for faster responses)
- `OpenAIWebSearchTool` - Web search capabilities for additional information
- `check_prerequisites` - Checks if you've completed prerequisites for a course
- `search_courses` - Searches for courses by name or code
- `get_completed_courses` - Retrieves your completed courses from your profile

