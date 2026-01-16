import json
from Chains.main_agent import main_agent_chain
from langchain.messages import AIMessage, SystemMessage
from state import MessagesState
from constants import LAST
from app.mongo import Users
from utilities.error_handlers import is_json_schema_error


def main_agent_node(state: MessagesState) -> MessagesState:
    try:
        if isinstance(state["messages"][LAST], AIMessage):
            return {**state}
        else:
            user = state["user"]
            user_data = Users.find_one({"username": user})
            name = user_data["name"]
            user_history = "\n".join(user_data["user_history"])

            res = main_agent_chain.invoke(
                {
                    "messages": state["messages"],
                    "name": name,
                    "user_history": user_history,
                }
            )
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
    except Exception as e:
        print(f"Error occured as : {e}")

        if is_json_schema_error(e):
            plain_msg = str(e)[224:-3]
            return {**state, "messages": [AIMessage(plain_msg)]}

        else:
            raise
