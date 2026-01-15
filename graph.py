from langgraph.graph import StateGraph
from state import MessagesState
from Nodes.main_agent_node import main_agent_node
from Nodes.suggestion_node import suggestion_node
from Nodes.get_destination_details_node import get_destination_details_node
from Nodes.hotel_flight_search_node import hotel_flight_node
from Nodes.text_summerrizer_node import summerizer
from constants import (
    MAIN_AGENT,
    END,
    LAST,
    SUGGESTION,
    GET_DESTINATION_DETAILS,
    HOTEL_FLIGHT,
    SUMMARIZATION,
)
from Conditional_edges.ce_main import diverter_main
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

load_dotenv(override=True)

graph = StateGraph(MessagesState)

memory = MemorySaver()

graph.add_node(MAIN_AGENT, main_agent_node)
graph.add_node(SUGGESTION, suggestion_node)
graph.add_node(GET_DESTINATION_DETAILS, get_destination_details_node)
graph.add_node(HOTEL_FLIGHT, hotel_flight_node)
graph.add_node(SUMMARIZATION, summerizer)

graph.set_entry_point(MAIN_AGENT)
graph.add_conditional_edges(
    MAIN_AGENT,
    diverter_main,
    path_map={
        SUGGESTION: SUGGESTION,
        GET_DESTINATION_DETAILS: GET_DESTINATION_DETAILS,
        HOTEL_FLIGHT: HOTEL_FLIGHT,
        SUMMARIZATION: SUMMARIZATION,
        MAIN_AGENT: MAIN_AGENT,
    },
)
graph.add_edge(SUGGESTION, MAIN_AGENT)
graph.add_edge(GET_DESTINATION_DETAILS, MAIN_AGENT)
graph.add_edge(HOTEL_FLIGHT, MAIN_AGENT)
graph.add_edge(SUMMARIZATION, END)

app = graph.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}

app.get_graph().draw_mermaid_png(output_file_path="GRAPHS-PNGs/flow-6.png")


async def responder(user_input, history=[]):
    user = "ais"
    res = await app.ainvoke(
        {"messages": [HumanMessage(content=user_input)], "user": user},
        config=config,
    )
    return res["messages"][LAST].content


# async def responder(user_input: str, user: str):
#     res = await app.ainvoke(
#         {"messages": [HumanMessage(content=user_input)], "user": user}, config=config
#     )
#     return {"message": res["messages"][LAST].content}
