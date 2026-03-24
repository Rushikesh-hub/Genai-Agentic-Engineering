from agent.multi_agents.researcher import researcher_agent
from agent.multi_agents.analyst import analyst_agent
from agent.multi_agents.writer import writer_agent


def run_multi_agent_system(goal):

    print("\n[Researcher working...]\n")
    research_data = researcher_agent(goal)

    print("\n[Analyst working...]\n")
    analysis = analyst_agent(research_data)

    print("\n[Writer working...]\n")
    final_output = writer_agent(analysis)

    return final_output