from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import END

load_dotenv(override=True)

# LLMs
LLM1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
LLM2 = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
LLM3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
LLM4 = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", temperature=0)
LLM5 = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

# Nodes
MAIN_AGENT = "main_agent"
GET_DESTINATION_DETAILS = "get_destination_details"
SUGGESTION = "suggestion"
SUMMARIZATION = "summarization"
END = END

# Mics
LAST = -1
HOTEL_FLIGHT = "hotel_flight_assistance"
PROFILE_PHOTO_DIR = "app/images/profile-photos"
CLIENT = MultiServerMCPClient(
    {
        "local_tools": {
            "command": "python",
            "args": ["MCP_Servers/weather_tavily_mcp_server.py"],
            "transport": "stdio",
        }
    }
)
