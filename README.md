Achieve — AI Learning Coach
Achieve is a Python-based AI-powered coaching assistant that helps users master any skill or goal by generating personalized weekly roadmaps, assignments, and curated resources. It uses OpenAI's GPT models and LangChain to guide users through structured, trackable learning plans.

FEATURES:

Personalized goal planning with structured weekly checkpoints

Resource-rich assignments (videos, articles, courses)

Time-based planning based on user input (skill level, daily time, duration)

Success criteria and progress tracking metrics

Built using LangChain, Pydantic, and OpenAI's GPT models

REQUIREMENTS:

Python 3.10+

OpenAI API key

Libraries: langchain, langchain-openai, pydantic, dotenv, etc.

Install dependencies:
pip install -r requirements.txt

GETTING STARTED:

Clone the repo:
git clone https://github.com/yourusername/achieve.git
cd achieve

Create a .env file in the root directory and add your OpenAI key:
OPENAI_API_KEY=your-api-key-here

Run the program:
python main.py

Follow the prompts to generate a personalized learning roadmap.

TECH STACK:

LangChain — for orchestrating LLM workflows

OpenAI GPT-4o-mini — LLM engine

Pydantic — for strict data structure parsing and validation

dotenv — environment variable management

JSON — data persistence

OUTPUT:
Each user interaction generates a structured roadmap file saved as:
data/user_roadmap.json

UPCOMING FEATURES:

Tool integrations like Tavily to find relevant online tutorials and articles

Personalized memory and learning rate adaptation

Progress tracking dashboard or app UI

Export roadmap to calendar or to-do managers

LICENSE:
MIT License. See LICENSE file for details.

Made with 🧠 by Evan Blunt