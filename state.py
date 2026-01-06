from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    need_clarification: bool
    need_suggestion: bool
    tools: list
    need_destination_details: bool
    user_preferences: str
    destination_query: str
