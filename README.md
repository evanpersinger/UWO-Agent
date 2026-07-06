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

- **uv** - Python package & project manager. Install from [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/) or with `curl -LsSf https://astral.sh/uv/install.sh | sh`. Check with: `uv --version`. uv will automatically install a compatible Python (3.11+) for you.
- **Git** - For cloning the repository. Check with: `git --version`
- **OpenAI API Key** - Required for the agent to function. Get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

If any of these are missing, install them before proceeding with the installation.

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd uwo_course_repo
```

2. Install dependencies:

```bash
uv sync
```

This creates a virtual environment in `.venv` and installs everything pinned in `uv.lock`.

## Setup

**Important:** The agent requires an OpenAI API key to function. Without it, the agent will not work.

1. Create a `.env` file in the project root
2. Add your OpenAI API key (get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)):

```
OPENAI_API_KEY=your_api_key_here
```

3. Copy the profile template, then fill it in with your information (e.g., your program, year, courses you've taken, etc.) so the agent can provide personalized advice:

```bash
cp user_profile_example.md user_profile.md
```

Your `user_profile.md` is gitignored, so your personal info stays local and is never committed. Edit `user_profile.md` (not the example) with your details.

## Usage

1. Make sure you've completed the Setup steps above (created `.env` file and filled in `user_profile.md`)

2. Run the agent:

```bash
uv run python agent.py
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
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Pinned, fully-resolved dependency versions (managed by uv)
- `.env` - Environment variables (create this file with your API key)
- `user_profile_example.md` - Template for your student profile (tracked in git)
- `user_profile.md` - Your personal profile; copy it from the example and fill it in (gitignored, never committed)

## Tools

The agent has access to:
- `fetch_url` - Fetches content from Western University course calendar URLs (with caching for faster responses)
- `WebSearchTool` - Web search capabilities for additional information
- `check_prerequisites` - Checks if you've completed prerequisites for a course
- `search_courses` - Searches for courses by name or code
- `get_completed_courses` - Retrieves your completed courses from your profile

