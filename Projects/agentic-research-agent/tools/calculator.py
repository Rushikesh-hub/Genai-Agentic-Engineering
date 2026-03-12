def calculator_tool(expression: str):

    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid calculation"