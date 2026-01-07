from state import MessagesState
from langchain.agents import create_agent
from constants import LAST, LLM3, CLIENT
from Chains.suggestion import suggestion_prompt


async def suggestion_node(state: MessagesState) -> MessagesState:
    user_taste = state["user_preferences"]
    tools = await CLIENT.get_tools()
    suggestion_agent = create_agent(model=LLM3, tools=tools)
    suggestion_chain = suggestion_prompt | suggestion_agent
    all_messages = await suggestion_chain.ainvoke({"user_taste": user_taste})
    res = all_messages["messages"][LAST]
    return {
        "messages": res["messages"] if isinstance(res, dict) else [res],
        "need_suggestion": False,
    }
