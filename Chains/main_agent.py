from email import message
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from constants import LLM2
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

today = datetime.now().strftime("%A, %d %B %Y")

main_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are travel guide assistant at Ais Travel Guide Company,
            Today : {today}
    Task: 
    - Greet user well and politely ask how can you help, wheather he has any prefrence for any place to travel or he wants you to suggest travel         destination for him.
    - If the user wants you to suggest travel destination for him, clarify from them following points in Markdown:

            Activities they enjoy
            (trekking, camping, wildlife, water sports, snow sports, sightseeing, food, nightlife)

            Travel intent / mood 
            (peace, adventure, relaxation, romance, spirituality, party, exploration)

            Preferred terrain or geography
            (mountains, beach, desert, forest, island, countryside, city, mixed)

            Travel style
            (solo, couple, family, friends, business)

            Budget range
            (budget, mid-range, luxury)

            Timing
            (when does the user want to go for this trip)

            Trip duration

            any other(if provided by user himself)

    - Infer obvious attributes from user preferences instead of asking. Example: paragliding → mountains + adventure.
    - If user express that he does not want to travel particular places or does not like particular places, you should mention these destinations in user_taste in structured output.
    - When you are done with all the clarification from user and there is no further quesion, don't generate the suggestion answer, your sub Agent will reply to the user about the suggestions according to user taste.
    - If user already has a preference for a desination or he selects a destination from the suggestions, Always ask him first weather he wants to know more about that destination like culture, tourist activities, local food, places to visit, itenary etc. If user wants to know more, turn need_destination_details in structured output to be 'True' ,and don't generate the detailed answer, your sub Agent will reply to the user with the complete details of the destination.
    """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
).partial(today=today)


class SchemaMain(BaseModel):
    messages: str = Field(
        description="Conversation message either answer or clarification queation by AI assistant"
    )
    need_suggestion: bool = Field(
        description="True- only if user wants AI assitant to find travel destination for him, or user do not like current suggestion and need further suggestions else False"
    )
    need_clarification: bool = Field(
        description="False: only when no further clarification about user's taste for travel destinaion required by AI assitant and AI assistant is satisfied to give suggestion, else True"
    )
    user_taste: Optional[str] = Field(
        None,
        description="Structured representation of user travel preferences and also destinations_to_avoid(if user say he doesn't prefer particular places), example:'intent: peace; terrain: mountains; activities: sightseeing; travel_style: solo; budget: budget; destinations_to_avoid: Manali, Shimla, Kufri; etc.",
    )
    destination: Optional[str] = Field(
        None,
        description="The destination, already preferred by user or selected from suggestions. Write only valid destination name, correct it if user has made a spelling mistake or written invalid name. Example : valid name is Bir while people write it as Bir-Billing, which are two different places",
    )
    need_destination_details: bool = Field(
        description="True : only when user wants more details about the destination already preferred or choosen from suggestion, else : False "
    )


llm_structured = LLM2.with_structured_output(SchemaMain, method="json_schema")

main_agent_chain = main_agent_prompt | llm_structured
