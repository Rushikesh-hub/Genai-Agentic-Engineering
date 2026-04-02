from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def evaluate_response(query, response):

    prompt = f"""
You are an AI evaluator.

Evaluate the response based on:

1. Relevance to the question
2. Correctness
3. Clarity

Return JSON:

{{
 "relevance": score (1-10),
 "correctness": score (1-10),
 "clarity": score (1-10),
 "hallucination": YES or NO
}}

Question:
{query}

Response:
{response}
"""

    result = llm.invoke(prompt)

    return result.content