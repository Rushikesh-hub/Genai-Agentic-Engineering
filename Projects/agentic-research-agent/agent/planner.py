from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def create_plan(goal: str):

    prompt = f"""
You are a task planner.

Break the goal into steps in JSON format.

Format:
[
  {{"step": "description"}},
  {{"step": "description"}}
]

Goal:
{goal}
"""

    response = llm.invoke(prompt)

    try:
        plan = json.loads(response.content)
    except:
        print("⚠️ Failed to parse plan, retrying...")
        return create_plan(goal)

    return plan