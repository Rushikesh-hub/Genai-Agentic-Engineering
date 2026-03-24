from langchain_openai import ChatOpenAI
from tools.web_search import web_search_tool

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def researcher_agent(query):

    search_results = web_search_tool(query)

    prompt = f"""
You are a research agent.

Use the following data to extract useful insights.

Data:
{search_results}

Provide key findings.
"""

    response = llm.invoke(prompt)

    return response.content