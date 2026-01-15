from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_agent
from Chains.hotel_flight_search import hotel_flight_search_prompt
from langchain_core.messages import HumanMessage
from constants import LLM4, CLIENT, LAST
from state import MessagesState
import asyncio


async def hotel_flight_node(state: MessagesState) -> MessagesState:
    user_query = state["hotels_flight_query"]
    user = state["user"]
    tools = await CLIENT.get_tools()
    hotel_search_agent = create_agent(model=LLM4, tools=tools)
    hotel_search_chain = hotel_flight_search_prompt | hotel_search_agent
    all_messages = await hotel_search_chain.ainvoke(
        {"user_query": user_query, "user": user}
    )
    res = all_messages["messages"][LAST]
    state["need_hotel_flight_node"] = False
    return {
        **state,
        "messages": [res],
        "need_clarification": False,
        "need_destination_details": False,
        "need_hotel_flight_node": False,
        "need_suggestion": False,
    }
