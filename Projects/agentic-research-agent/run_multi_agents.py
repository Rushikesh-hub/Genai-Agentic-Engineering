from agent.multi_agents.orchestrator import run_multi_agent_system

print("\nMulti-Agent System Ready!\n")

while True:

    goal = input("Enter your goal: ")

    if goal.lower() in ["exit", "quit"]:
        break

    result = run_multi_agent_system(goal)

    print("\n=== FINAL OUTPUT ===\n")
    print(result)