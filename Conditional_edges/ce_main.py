from state import MessagesState
from constants import (
    END,
    SUGGESTION,
    GET_DESTINATION_DETAILS,
    HOTEL_FLIGHT,
    SUMMARIZATION,
)


def diverter_main(state: MessagesState) -> str:
    if state.get("need_suggestion", False) and not state.get(
        "need_clarification", True
    ):
        return SUGGESTION
    elif state.get("need_destination_details", False):
        return GET_DESTINATION_DETAILS
    elif state.get("need_hotel_flight_node", False):
        return HOTEL_FLIGHT
    else:
        return SUMMARIZATION
