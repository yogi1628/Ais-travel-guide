from state import MessagesState
from constants import CLIENT
from Chains.destination_details import get_details_chain


async def get_destination_details_node(state: MessagesState) -> MessagesState:
    destination = state["destination"]
    tools = await CLIENT.get_tools()
    tool_map = {tool.name: tool for tool in tools}
    weather_info = await tool_map["weather_info"].ainvoke({"city": destination})
    wiki_result = await tool_map["get_wikivoyage_page"].ainvoke(
        {"destination": destination}
    )

    res = await get_details_chain.ainvoke(
        {
            "destination": destination,
            "weather_info": weather_info,
            "raw_content": wiki_result,
        }
    )
    return {
        "messages": res["messages"] if isinstance(res, dict) else [res],
        "need_suggestion": False,
        "user_taste": state["user_taste"],
        "need_clarification": state["need_clarification"],
        "destination": state["destination"],
        "need_destination_details": False,
    }
