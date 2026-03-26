from agent.router import route_query
from agent.rag_agent import rag_agent
from tools.web_search import web_search_tool
from tools.calculator import calculator_tool

from agent.multi_agents.analyst import analyst_agent
from agent.multi_agents.writer import writer_agent

from agent.memory_store.memory_manager import store_memory, retrieve_memory


def run_dynamic_system(query):

    # 🔹 Step 1: Retrieve memory
    past_context = retrieve_memory(query)

    print(f"\n[Memory Retrieved]: {past_context}\n")

    decision = route_query(query)

    print(f"\n[Router Decision: {decision}]\n")

    if decision == "SEARCH":

        data = web_search_tool(query)
        analysis = analyst_agent(data)
        result = writer_agent(analysis)

    elif decision == "RAG":

        result = rag_agent(query)

    elif decision == "CALCULATOR":

        result = calculator_tool(query)

    else:
        result = "Could not determine route"

    # 🔹 Step 2: Store memory
    store_memory(f"Q: {query} | A: {result}")

    return result