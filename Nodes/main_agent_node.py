from Chains.main_agent import main_agent_chain
from langchain.messages import AIMessage
from state import MessagesState
from constants import LAST


def main_agent_node(state: MessagesState) -> MessagesState:
    if isinstance(state["messages"][LAST], AIMessage):
        return
    else:
        res = main_agent_chain.invoke({"messages": state["messages"]})
        return {
            "messages": [AIMessage(res.messages)],
            "need_suggestion": res.need_suggestion,
            "user_taste": res.user_taste,
            "need_clarification": res.need_clarification,
            "destination": res.destination,
            "need_destination_details": res.need_destination_details,
        }
