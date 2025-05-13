from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from assistant.ros_tools import create_node, create_package

llm = ChatOpenAI(temperature=0.2, model="gpt-4")

tools = [
    Tool(name="CreateNode", func=create_node, description="Create a ROS 2 node"),
    Tool(name="CreatePackage", func=create_package, description="Create a ROS 2 package"),
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def handle_input(user_input):
    return agent.run(user_input)
