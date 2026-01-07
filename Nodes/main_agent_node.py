from Chains.main_agent import main_agent_chain
from langchain.messages import AIMessage
from state import MessagesState
from constants import LAST


def main_agent_node(state: MessagesState) -> MessagesState:
    if isinstance(state["messages"][LAST], AIMessage):
        return
    else:
        res = main_agent_chain.invoke({"messages": state["messages"]})
        print(state, res)
        return {
            "messages": [AIMessage(res.messages)],
            "need_suggestion": res.need_suggestion,
            "need_clarification": res.need_clarification,
            "need_destination_details": res.need_destination_details,
            "user_preferences": res.user_preferences,
            "destination_query": res.destination_query,
            "need_hotel_flight_node": res.need_hotel_flight_node,
            "hotels_flight_query": res.hotels_flight_query,
        }
