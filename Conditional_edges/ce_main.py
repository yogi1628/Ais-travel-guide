from state import MessagesState
from constants import END, SUGGESTION, GET_DESTINATION_DETAILS, HOTEL_FLIGHT


def diverter_main_suggestion(state: MessagesState) -> str:

    if not state.get("need_clarification", True) and state.get(
        "need_suggestion", False
    ):

        return SUGGESTION
    else:
        print(state)
        return END


def diverter_main_destination_details(state: MessagesState) -> str:
    return (
        GET_DESTINATION_DETAILS if state.get("need_destination_details", False) else END
    )


def diverter_main_hotel_flights(state: MessagesState) -> str:
    return HOTEL_FLIGHT if state.get("need_hotel_flight_node", False) else END
