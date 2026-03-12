def search_tool(query: str):

    # mock search results
    database = {
        "ai trends": "AI trends include generative AI, multimodal models, and agentic systems.",
        "rag": "Retrieval Augmented Generation combines retrieval with LLM generation.",
        "agentic ai": "Agentic AI systems allow LLMs to use tools and perform multi-step reasoning."
    }

    return database.get(query.lower(), "No results found")