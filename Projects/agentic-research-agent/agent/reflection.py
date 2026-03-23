from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def reflect(step, result):

    prompt = f"""
You are an evaluator.

Step:
{step}

Result:
{result}

Is this result correct and useful?

Answer ONLY:
- YES
- NO
"""

    response = llm.invoke(prompt)

    return response.content.strip()