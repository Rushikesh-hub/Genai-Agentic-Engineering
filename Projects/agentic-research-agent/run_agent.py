from agent.planner import create_plan
from agent.executer import execute_plan

print("\nTask Planning Agent Ready!\n")

while True:

    goal = input("Enter your goal: ")

    if goal.lower() in ["exit", "quit"]:
        break

    print("\n--- Creating Plan ---\n")

    plan = create_plan(goal)

    print(plan)

    print("\n--- Executing Plan ---\n")

    results = execute_plan(plan)

    print("\n--- Final Results ---\n")

    for r in results:
        print(f"\nStep: {r['step']}")
        print(f"Result: {r['result']}")