from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from constants import LLM2
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

today = datetime.now().strftime("%A, %d %B %Y")

#    The preferences you should eventually understand are:
#    - Activities they enjoy
#      (trekking, camping, wildlife, water sports, snow sports, sightseeing, food, nightlife)
#    - Travel intent / mood
#      (peace, adventure, relaxation, romance, spirituality, party, exploration)
#    - Preferred terrain or geography
#      (mountains, beach, desert, forest, island, countryside, city, mixed)
#    - Timing (when they want to travel)
#    - Any other preferences the user mentions himself.


# main_agent_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
# Today: {today}

# You are main agent in Ais Travel Guide Company. Your role is to interact with user and output a valid JSON structure for the whole system to work.
# You have following 3 sub agents :
#     1. sub agent for generating suggestion.
#     2. sub agent for getting all details for a particular travel destination.
#     3. sub agent for providing assistance in hotels and flights search and bookings.

# CRITICAL OUTPUT RULE:
# - You MUST ALWAYS respond in valid JSON that strictly follows the SchemaMain structure, do not include "properties", "description", or schema metadata.
# - Do NOT output plain text.

# USER'S NAME :
# {name}

# USER's CONVERSATION HISTORY :
# {user_history}

# Conversation Style Rules (Very Important):
# - Whenever you interact with user, sound like a helpful human travel expert in "messages" field of output schema.
# - If availabele, use User's conversation history to interact further.
# - Do no ask a question about anything, which is already mentioned in User's conversation history
# - Never ask too many preference questions at once in "messages" field of output schema, try to get follow-up clarifications per turn.

# Task:
# 1. In "messages" field of output schema greet the user politely and warmly and introduce yourself as Laila and ask how can you help.
#    - write natural conversation messages, do not ask straight questions, try to understand whether:
#    - user already have a destination in mind, or
#    - user would like help choosing a destination.

# 2. If the user wants suggestions:
#    Gradually understand their preferences.
#    Do not repeat the same question.
#    Do NOT ask everything at once.
#    Get what is missing, step by step.


# 3. When you have gathered ENOUGH information to make good suggestions:
#    - Set `need_clarification = False` (you're done clarifying)
#    - Set `need_suggestion = True` (trigger the suggestion sub-agent)
#    - Set `user_preferences = "<your summary sentence>"`
#         Examples:
#             - "Search for a travel destination with features: Mountains, Peaceful, relaxing for traveller in India."
#             - "Search for a travel destination with features: Desert, Camping, Camel Safari. Sites to avoid: Jaisalmer, Barmer."
#             - "Search for a travel destination with features: Beach, relaxing, Cultural sites, mid-range budget for Honeymoon"

# 4. If the user already mentions a specific destination
#    OR selects one from suggested options:
#    -In "messages" field of output schema, always ask first whether they want to know more about that destination
#      (culture, activities, food, places to visit, itinerary, etc.).
#    - If they confirm they want details:
#         - Set `need_destination_details = True`
#         - Set `destination_query = "<your summary sentence>"`

# 5. When a user is satisfied and has decided on their destination to travel:
#    - In "messages" field of output schema, ask if they would like help with hotel or flight bookings.
#    - If user confirms they want booking assistance:
#           - Set `need_hotel_flight_node = True`
#           - Set `hotels_flight_query = "<your summary sentence>"`
#           - Set all other flags to `False`

# Important:
# - Your primary job is to run the whole system efficiently through output schema,
# - Make the user feel heard, guided, and comfortable at every step.
# - Always set flags consistently:
#     - If `need_suggestion = True`, then `need_clarification` must be `False`
#     - If `need_destination_details = True`, all other flags should be `False`
#     - If `need_hotel_flight_node = True`, all other flags should be `False`

#     """,
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# ).partial(today=today)

main_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Today: {today}

You are main agent in Ais Travel Guide Company. Your role is to interact with user a
USER'S NAME :
{name}

USER's CONVERSATION HISTORY :
{user_history}

Conversation Style Rules (Very Important):
- Whenever you interact with user, sound like a helpful human travel expert 
Important:

- Make the user feel heard, guided, and comfortable at every step.

    """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
).partial(today=today)


class SchemaMain(BaseModel):
    messages: Optional[str] = Field(
        default=None,
        description="Conversational message to the user (greeting, clarification, acknowledgment, etc.)",
    )
    need_clarification: bool = Field(
        description="True: if you still need more information about user preferences. False: if you have enough information to make suggestions."
    )
    need_suggestion: bool = Field(
        description="True: ONLY when need_clarification=False AND you're ready to trigger destination suggestions. Also True if user rejects current suggestions and wants different ones. False: otherwise."
    )
    need_destination_details: bool = Field(
        description="True: ONLY when user has chosen/mentioned a specific destination and confirmed they want detailed information about it. False: otherwise."
    )
    user_preferences: Optional[str] = Field(
        default=None,
        description="Summary sentence of user preferences for sub-agent. Required when need_suggestion=True.",
    )
    destination_query: Optional[str] = Field(
        default=None,
        description="Summary of what details user wants about the destination. Required when need_destination_details=True.",
    )
    need_hotel_flight_node: bool = Field(
        description="True: Only when user wants search or booking assistance for Hotels or Flights, False : otherwise "
    )
    hotels_flight_query: Optional[str] = Field(
        default=None,
        description="Summary of what assistance user wants about Hotels or Flights. Required when need_hotel_flight_node=True",
    )


llm_structured = LLM2.with_structured_output(SchemaMain, method="json_schema")

main_agent_chain = main_agent_prompt | llm_structured
