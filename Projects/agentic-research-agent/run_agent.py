from agent.agent import agent

print("\nAgent Ready! Ask anything.\n")

while True:

    query = input("You: ")

    if query.lower() in ["exit", "quit"]:
        break

    response = agent.run(query)

    print("\nAgent:", response, "\n")