from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import END

load_dotenv(override=True)

LLM1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
LLM2 = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
LLM3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
MAIN_AGENT = "main_agent"
GET_DESTINATION_DETAILS = "get_destination_details"
END = END
SUGGESTION = "suggestion"
LAST = -1
MCP_INIT = "mcp_init"
CLIENT = MultiServerMCPClient(
    {
        "local_tools": {
            "command": "python",
            "args": ["MCP_Servers/weather_tavily_mcp_server.py"],
            "transport": "stdio",
        }
    }
)
