import os
import community

# 加载环境变量
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

from langchain_deepseek import ChatDeepSeek
from langchain.tools import tool

#引入搜索工具
from tools import serpapi_search_tool

tools = [serpapi_search_tool]

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=3,
    timeout=None,
    max_retries=2,
)

DS_llm = llm.bind_tools(tools)

#定义state
from langchain.messages import AnyMessage
from typing_extensions import TypedDict,Annotated
import operator

class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

#定义放射科医生节点
import prompts
from langchain.messages import SystemMessage

def radiology_agent(state: dict):
    """
    放射科医生智能体 - 肺结节CT影像诊断专家
    """
    return{
        "messages":[
            DS_llm.invoke(
                [
                    SystemMessage(content=prompts.radiology_prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def respiratory_agent(state: dict):
    """
    呼吸科医生智能体 - 肺结节CT影像诊断专家
    """
    return{
        "messages":[
            DS_llm.invoke(
                [
                    SystemMessage(content=prompts.respiratory_prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def pathology_agent(state: dict):
    """
    病理科医生智能体 - 肺结节CT影像诊断专家
    """
    return{
        "messages":[
            DS_llm.invoke(
                [
                    SystemMessage(content=prompts.pathology_prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def thoracic_agent(state: dict):
    """
     thoracic医生智能体 - 肺结节CT影像诊断专家
    """
    return{
        "messages":[
            DS_llm.invoke(
                [
                    SystemMessage(content=prompts.toracic_prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def radiation_agent(state: dict):
    """
    放射科医生智能体 - 肺结节CT影像诊断专家
    """
    return{
        "messages":[
            DS_llm.invoke(
                [
                    SystemMessage(content=prompts.radiation_prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def rehabilitation_agent(state: dict):
    """
    康复科医生智能体 - 肺结节CT影像诊断专家
    """
    return{
        "messages":[
            DS_llm.invoke(
                [
                    SystemMessage(content=prompts.rehabilitation_prompt)
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


#建立agent

agent_builder = StateGraph(MessageState)

agent_builder.add_node("radiology_agent", radiology_agent)
agent_builder.add_node("respiratory_agent", respiratory_agent)
agent_builder.add_node("pathology_agent", pathology_agent)
agent_builder.add_node("thoracic_agent", thoracic_agent)
agent_builder.add_node("radiation_agent", radiation_agent)
agent_builder.add_node("rehabilitation_agent", rehabilitation_agent)

agent_builder.add_edge("radiology_agent", "respiratory_agent")
agent_builder.add_edge("respiratory_agent", "pathology_agent")
agent_builder.add_edge("pathology_agent", "thoracic_agent")
agent_builder.add_edge("thoracic_agent", "radiation_agent")
agent_builder.add_edge("radiation_agent", "rehabilitation_agent")


agent = agent_builder.compile()

from IPython.display import Image, display

display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

from langchain.messages import HumanMessage
messages = [HumanMessage(content=query)]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()