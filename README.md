# UWO Course Research Agent

An AI agent that helps students research courses at Western University. The agent can answer questions about course prerequisites, descriptions, syllabi, and other course-related information.

## Features

- Answer questions about Western University courses
- Access course information from the Western University calendar
- Search the web for additional course information
- Help with prerequisites, co-requisites, and antirequisites
- Provide course descriptions and syllabus information

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Create a `.env` file in the project root
2. Add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the agent:

```bash
python agent.py
```

The agent will start a REPL loop where you can ask questions about Western University courses. Type your questions and the agent will help you find the information you need.

## Project Structure

- `agent.py` - Main agent implementation
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file with your API key)

## Tools

The agent has access to:
- `fetch_url` - Fetches content from Western University course calendar URLs
- `OpenAIWebSearchTool` - Web search capabilities for additional information

