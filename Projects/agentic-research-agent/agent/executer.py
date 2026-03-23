from agent.agent import agent
from agent.reflection import reflect


def execute_plan(plan):

    results = []

    for task in plan:

        step = task["step"]

        print(f"\nExecuting: {step}")

        retries = 2
        success = False

        while retries > 0 and not success:

            result = agent.run(step)

            evaluation = reflect(step, result)

            print(f"Reflection: {evaluation}")

            if "YES" in evaluation.upper():
                success = True
            else:
                print("Retrying step...")
                retries -= 1

        results.append({
            "step": step,
            "result": result,
            "status": "success" if success else "failed"
        })

    return results