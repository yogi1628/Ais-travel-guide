from state import MessagesState
from langchain.agents import create_agent
from constants import LAST, LLM2, CLIENT
from Chains.suggestion import suggestion_prompt


async def suggestion_node(state: MessagesState) -> MessagesState:
    # user_taste = state["user_taste"]
    user_taste = state["messages"][LAST].content
    tools = await CLIENT.get_tools()
    suggestion_agent = create_agent(model=LLM2, tools=tools)
    suggestion_chain = suggestion_prompt | suggestion_agent
    all_messages = await suggestion_chain.ainvoke({"user_taste": user_taste})
    res = all_messages["messages"][LAST]
    return {
        "messages": res["messages"] if isinstance(res, dict) else [res],
        "need_suggestion": False,
        # "user_taste": state["user_taste"],
        "user_taste": user_taste,
        "need_clarification": state["need_clarification"],
        "destination": state["destination"],
        "need_destination_details": state["need_destination_details"],
    }
