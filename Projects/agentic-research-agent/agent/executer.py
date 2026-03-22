from agent.agent import agent

def execute_plan(plan: str):

    steps = plan.split("\n")

    results = []

    for step in steps:

        if step.strip() == "":
            continue

        print(f"\nExecuting: {step}")

        result = agent.run(step)

        results.append({
            "step": step,
            "result": result
        })

    return results