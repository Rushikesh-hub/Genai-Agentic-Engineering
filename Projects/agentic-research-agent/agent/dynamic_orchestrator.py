from agent.router import route_query
from agent.rag_agent import rag_agent
from tools.web_search import web_search_tool
from tools.calculator import calculator_tool

from agent.multi_agents.analyst import analyst_agent
from agent.multi_agents.writer import writer_agent


def run_dynamic_system(query):

    decision = route_query(query)

    print(f"\n[Router Decision: {decision}]\n")

    if decision == "SEARCH":

        data = web_search_tool(query)
        analysis = analyst_agent(data)
        final = writer_agent(analysis)
        return final

    elif decision == "RAG":

        return rag_agent(query)

    elif decision == "CALCULATOR":

        return calculator_tool(query)

    else:
        return "Could not determine route"