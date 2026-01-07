import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import json
import os
import requests
from amadeus_cl import hotel_search

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
    """
    Fetch a plain-text travel guide summary for a destination from Wikivoyage.

    Args:
        destination (str): Destination name (e.g., "Paris", "Kerala").

    Returns:
        str: Wikivoyage page extract if available, otherwise an invalid
             destination message.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request fails.
        ValueError: If a non-JSON response is received.
    """
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
    response.raise_for_status()
    if not response.headers.get("Content-Type", "").startswith("application/json"):
        raise ValueError("Non-JSON response received")
    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    return (
        page.get("extract")
        if page.get("extract") != None
        else f"Invalid name : {destination}, Try with a valid name"
    )


@mcp.tool()
def get_hotels_by_geo_code(
    lat: float, lon: float, ratings: list[str] = ["3", "4", "5"]
) -> list:
    """
    Search hotels near a geographic location using latitude and longitude.

    Use this tool when the user provides coordinates instead of a city name.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        ratings (list[str], optional): Hotel star ratings to filter by.

    Returns:
        list: List of hotels near the given coordinates,
        or a fallback message if no hotels are found.
    """
    hotels = hotel_search.search_hotels_by_geocode(
        latitude=lat, longitude=lon, radius=5, ratings=ratings
    )
    return (
        ["Hotels not found from this tool, Try Tavilly Search tool."]
        if hotels == []
        else hotels
    )


@mcp.tool()
def get_hotel_by_city_code(
    city_code: str,
    ratings: list[str] = ["3", "4", "5"],
    amenities: list[str] = ["WIFI"],
) -> list:
    """
    Search hotels within a city using IATA city code.

    Use this tool when the user specifies a destination city.

    Args:
        city_code (str): City code identifier.
        ratings (list[str], optional): Hotel star ratings to filter by.
        amenities (list[str], optional): Required hotel amenities.

    Returns:
        list: List of hotels in the city,
        or a fallback message if no hotels are found.
    """
    hotels = hotel_search.search_hotels_by_city(
        city_code=city_code, radius=20, ratings=ratings, amenities=amenities
    )
    return (
        ["Hotels not found from this tool, Try Tavilly Search tool."]
        if hotels == []
        else hotels
    )


# @mcp.tool()
# def hotel_offers(
#     hotel_ids: str,
#     check_in_date: str,
#     check_out_date: str,
#     adults: int,
#     room_quantity: int,
#     currency: str,
#     board_type: str = "BREAKFAST",
# ) -> list:
#     """
#     Fetch available hotel offers for given hotels and stay details.

#     Dates must be in YYYY-MM-DD format.

#     Args:
#         hotel_ids (str): list of Comma-separated hotel ID, e.g. : hotel_ids = ["RDSLV925","OBSLVCEC","QISLV055","OBSLVWFH"] .
#         check_in_date (str): Check-in date (YYYY-MM-DD).
#         check_out_date (str): Check-out date (YYYY-MM-DD).
#         adults (int): Number of adults.
#         room_quantity (int): Number of rooms.
#         currency (str): Currency code (e.g., INR, USD).
#         board_type (str, optional): Meal plan type.

#     Returns:
#         list: Available hotel offers matching the criteria.
#     """
#     offers = hotel_search.search_hotel_offers(
#         hotel_ids=hotel_ids,
#         check_in_date=check_in_date,
#         check_out_date=check_out_date,
#         adults=adults,
#         room_quantity=room_quantity,
#         currency=currency,
#         board_type=board_type,
#     )
#     if not offers:
#         return json.dumps({"success": False, "message": "No offers"})
#     return json.dumps({"success": True, "offers": offers})


if __name__ == "__main__":
    mcp.run(transport="stdio")
