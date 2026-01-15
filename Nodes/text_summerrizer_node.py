from langchain_core.messages import AIMessage, HumanMessage
from Chains.text_summerization import summerizer_chain
from state import MessagesState
from app.mongo import Users
from constants import LAST


async def summerizer(state: MessagesState) -> MessagesState:
    if len(state["messages"]) < 10:
        return {**state}
    else:
        user = state["user"]
        messages = ""
        for message in state["messages"]:
            messages = (
                messages + "\n" + f"AI: {message.content}"
                if isinstance(message, AIMessage)
                else messages + "\n" + f"Human: {message.content}"
            )
        res = await summerizer_chain.ainvoke({"messages": messages})
        summary = res.content
        Users.update_one(
            {"username": user},
            {"$push": {"user_history": summary}},
        )
        last_msg = state["messages"][LAST]
        state["messages"].clear()
        return {**state, "messages": [last_msg]}
