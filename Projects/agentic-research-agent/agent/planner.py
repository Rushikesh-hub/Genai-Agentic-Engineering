from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

def create_plan(goal: str):

    prompt = f"""
You are a task planner.

Break the following goal into clear step-by-step tasks.

Goal:
{goal}

Return steps as a numbered list.
"""

    response = llm.invoke(prompt)

    return response.content