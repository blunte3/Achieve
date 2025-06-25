from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_resources
import json
import os
import re

load_dotenv()
tools = [search_resources]

# -------------------- Data Models --------------------
class Resource(BaseModel):
    title: str
    type: str  # e.g., "video", "article", "course"
    url: str
    description: Optional[str] = None

class Assignment(BaseModel):
    description: str
    objective: str
    resources: List[Resource]
    estimated_time_minutes: int

class WeeklyCheckpoint(BaseModel):
    week: int
    title: str
    summary: str
    goals: List[str]
    assignments: List[Assignment]
    reflection_prompt: Optional[str] = None

class GoalResponse(BaseModel):
    user_goal: str = Field(..., description="The user's stated goal")
    duration_weeks: int = Field(..., description="The total duration in weeks (default 6)")
    skill_level: str = Field(..., description="Estimated starting skill level, e.g. 'beginner'")
    time_commitment_per_day_minutes: int = Field(..., description="User’s daily available time to work on this goal")
    overall_strategy: str = Field(..., description="A brief summary of the strategy to achieve this goal")
    weekly_checkpoints: List[WeeklyCheckpoint] = Field(..., description="Detailed weekly breakdown of roadmap")
    general_resources: List[Resource] = Field(..., description="General purpose resources for this goal")
    tracking_metrics: Optional[List[str]] = Field(default=None, description="Optional metrics for progress tracking")
    success_criteria: Optional[str] = Field(default=None, description="What constitutes success or completion of this goal")
    personalization_notes: Optional[str] = Field(default=None, description="Notes specific to this user’s learning preferences or habits")

# -------------------- LLM Setup --------------------
llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=GoalResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a world class goal-setting AI coach in the Achieve app. You are extremely knowledgable about any goal the user inputs.
            Your job is to help the user plan how to master a goal they care about as well.
            Use the following information from the user to create a detailed and structured GoalResponse roadmap:

            - user_goal: What the user wants to achieve.
            - skill_level: Their starting experience level (e.g., beginner, intermediate, advanced).
            - duration_weeks: How many weeks they want to work on it.
            - time_commitment_per_day_minutes: How much time per day they can dedicate to this goal.
            - personalization_notes: Any user preferences, learning styles, tools they like/dislike, or other constraints.
            
            Your output should include:
            - An overall strategy
            - Weekly checkpoints (title, summary, goals, assignments)
            - Assignments with time estimates and linked resources
            - Success criteria
            - General resources and tracking metrics if relevant

            You must return your result in this exact format:\n{format_instructions}
            """
        ),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# -------------------- Agent --------------------
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# -------------------- User Input --------------------
print("Welcome to Achieve — your AI learning coach. Let's set up your roadmap.")
user_goal = input("🎯 What goal do you want to achieve? ")
skill_level = input("🧠 What is your current skill level (beginner, intermediate, advanced)? ")
duration_weeks = input("📅 How many weeks do you want to work on this goal? ")
time_per_day = input("⏱️ How many minutes per day can you dedicate to this goal? ")
preferences = input("💬 Any preferences or notes? (e.g., I like video tutorials, I learn best by doing): ")

# Build the full query
query = f"""
The user's goal is: {user_goal}
Their current skill level is: {skill_level}
They want to work on this for {duration_weeks} weeks.
They have {time_per_day} minutes per day to dedicate.
Their learning preferences or notes are: {preferences}
"""

# -------------------- Invoke Agent --------------------
raw_response = agent_executor.invoke({"query": query})

try:
    output_str = raw_response.get("output", "")

    # Remove ```json ... ``` wrapper if it exists
    if isinstance(output_str, str) and output_str.strip().startswith("```"):
        output_str = re.sub(r"^```json\s*|\s*```$", "", output_str.strip(), flags=re.DOTALL)

    # Load string as JSON
    output_dict = json.loads(output_str)

    # Parse and validate
    structured_response = GoalResponse.model_validate(output_dict)

    print("\n✅ Success! Your roadmap has been generated.\n")
    print(structured_response.model_dump_json(indent=2))

    # -------------------- Save to File --------------------
    os.makedirs("data", exist_ok=True)
    with open("data/user_roadmap.json", "w") as f:
        json.dump(structured_response.model_dump(), f, indent=2)

except Exception as e:
    print("\n❌ Error parsing the response:", e)
    print("🧪 Cleaned output was:\n", output_str)
    print("📦 Full raw response:\n", raw_response)
