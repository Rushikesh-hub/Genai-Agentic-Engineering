from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def analyst_agent(data):

    prompt = f"""
You are an analyst.

Analyze the following data and extract patterns, trends, and insights.

Data:
{data}

Provide structured insights.
"""

    response = llm.invoke(prompt)

    return response.content