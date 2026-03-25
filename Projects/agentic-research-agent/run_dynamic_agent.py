from agent.dynamic_orchestrator import run_dynamic_system

print("\nDynamic Multi-Agent System Ready!\n")

while True:

    query = input("Enter your query: ")

    if query.lower() in ["exit", "quit"]:
        break

    result = run_dynamic_system(query)

    print("\n=== FINAL OUTPUT ===\n")
    print(result)