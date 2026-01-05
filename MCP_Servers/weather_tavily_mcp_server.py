import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import os
import requests

load_dotenv()

tavily = TavilySearch(
    max_results=5,
    search_depth="advanced",
    max_tokens=100,
)

mcp = FastMCP("local_tools")
owm_api_key = os.getenv("OPENWEATHERMAP_API_KEY")


@mcp.tool()
def tavily_search(query):
    """
    Perform a web search using the Tavily search tool.
    Use this function to retrieve up-to-date and relevant information from the web.
    Args:
        query (str): The search query describing the information to retrieve.
    Returns:
        dict: The raw response returned by the Tavily search tool, containing
        search results and associated metadata.
    """
    res = tavily.invoke({"query": query})
    return res


@mcp.tool()
def weather_info(city: str) -> dict:
    """
    Fetch real-time weather data for a given city using the OpenWeatherMap API.

    Use this tool when the user asks for current or live weather information
    (such as temperature, humidity, conditions, etc.) for a specific city.

    Args:
        city (str): Name of the city for which real-time weather data is requested.

    Returns:
        dict | str:
            - A dictionary containing weather data returned by the OpenWeatherMap API
              if the city is found successfully.
            - A user-friendly error message string if the city is not found or the
              request fails.
    """
    owm_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": owm_api_key, "units": "metric"}
    response = requests.get(owm_url, params=params)
    data = response.json()
    print(f"weather function called for {city} city")
    return data if data["cod"] == 200 else "Sorry, City not found"


@mcp.tool()
def get_wikivoyage_page(destination: str):
    HEADERS = {"User-Agent": "AisTravelGuide/1.0 (contact: your_email@example.com)"}
    url = "https://en.wikivoyage.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "titles": destination,
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1,
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=10)

    # 🔴 IMPORTANT: always check status
    response.raise_for_status()

    # 🔴 Ensure we actually received JSON
    if not response.headers.get("Content-Type", "").startswith("application/json"):
        raise ValueError("Non-JSON response received")

    data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    return page.get("extract")


if __name__ == "__main__":
    mcp.run(transport="stdio")
