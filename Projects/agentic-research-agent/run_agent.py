from agent.agent import agent

while True:

    query = input("\nAsk the agent: ")

    response = agent.run(query)

    print("\nAgent Response:\n", response)