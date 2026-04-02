import json
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


def evaluate_response(query, response):

    prompt = f"""
You are an AI evaluator.

Evaluate the response based on:

1. Relevance to the question
2. Correctness
3. Clarity

Return STRICT JSON format:

{{
 "relevance": number (1-10),
 "correctness": number (1-10),
 "clarity": number (1-10),
 "hallucination": "YES" or "NO"
}}

Question:
{query}

Response:
{response}
"""

    result = llm.invoke(prompt)

    try:
        return json.loads(result.content)
    except Exception:
        return {
            "error": "evaluation parsing failed",
            "raw_output": result.content
        }