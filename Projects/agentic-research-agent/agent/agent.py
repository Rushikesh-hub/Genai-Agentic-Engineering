from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import Tool

from tools.calculator import calculator_tool
from tools.web_search import web_search_tool

from agent.memory import memory


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


tools = [

    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for solving math problems"
    ),

    Tool(
        name="WebSearch",
        func=web_search_tool,
        description="Search the internet for current information"
    )
]


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=True
)