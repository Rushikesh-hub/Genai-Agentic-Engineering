from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def writer_agent(insights):

    prompt = f"""
You are a professional writer.

Create a clear, well-structured final report from the insights below.

Insights:
{insights}
"""

    response = llm.invoke(prompt)

    return response.content