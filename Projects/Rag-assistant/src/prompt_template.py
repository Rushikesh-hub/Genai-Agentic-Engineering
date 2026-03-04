def build_prompt(context_chunks, question):
    
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant that answers questions using the provided context.

Use ONLY the information from the context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt