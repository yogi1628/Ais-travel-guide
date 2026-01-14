from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from constants import LLM5

summerizer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You summarize travel-related conversations.

Input: Up to 8 recent Human–AI messages.
Output: EXACTLY one sentence, max 50 words.

Include only:
- Destinations, dates, duration
- Budget, travel style, activities
- Hotels, flights, bookings
- Recommendations the user showed interest in
- Decisions or near-decisions

Exclude:
- Greetings, small talk, repetitions
- AI reasoning or explanations
- Unconfirmed or ignored suggestions

Rules:
- No assumptions or new info
- Plain text only
- Preserve user intent and facts

Example :
    Human: I’m thinking about traveling in July but haven’t decided where.
    AI: Do you prefer mountains or beaches?
    Human: Mountains, somewhere cool and not too expensive.
    AI: Manali, Mussoorie, and Darjeeling fit well within a moderate budget.
    Human: Which one is best for a relaxed trip?

    Output : The user is planning a July trip, prefers a cool mountain destination on a moderate budget, and is seeking recommendations among Manali, Mussoorie, and Darjeeling for a relaxed vacation.


""",
        ),
        ("user", "Make a smart summary of the this conversation :\n {messages}"),
    ]
)

summerizer_chain = summerizer_prompt | LLM5
