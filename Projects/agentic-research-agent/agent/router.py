from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def route_query(query):

    prompt = f"""
You are a routing agent.

Decide which system should handle the query:

Options:
- SEARCH → for latest/current information
- RAG → for internal knowledge base
- CALCULATOR → for math

Return ONLY one word: SEARCH, RAG, or CALCULATOR

Query:
{query}
"""

    response = llm.invoke(prompt)

    return response.content.strip().upper()