from state import MessagesState
from constants import CLIENT, LAST, LLM2
from Chains.destination_details import destination_details_prompt
from langchain.agents import create_agent


async def get_destination_details_node(state: MessagesState) -> MessagesState:
    destination_query = state["destination_query"]
    tools = await CLIENT.get_tools()

    destination_detail_agent = create_agent(model=LLM2, tools=tools)
    get_details_chain = destination_details_prompt | destination_detail_agent

    res = await get_details_chain.ainvoke({"destination_query": destination_query})
    return {
        "messages": res["messages"] if isinstance(res, dict) else [res],
        "need_suggestion": False,
        "need_destination_details": False,
    }
