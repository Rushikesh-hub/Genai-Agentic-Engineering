from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import Tool

from tools.calculator import calculator_tool
from tools.search_tool import search_tool

llm = ChatOpenAI(model="gpt-4.1-mini")

tools = [

    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for performing mathematical calculations"
    ),

    Tool(
        name="Search",
        func=search_tool,
        description="Useful for searching information about AI topics"
    )
]


agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)