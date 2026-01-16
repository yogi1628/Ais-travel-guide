import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import json
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
def search_hotel(city: str, stars: int = None):
    """
    Search hotels by city and optional star rating.
    Args:
        city (str): City name.
        stars (int, optional): Hotel star rating.
    """
    url = (
        f"http://localhost:3000/hotels/{city}?stars={stars}"
        if stars
        else f"http://localhost:3000/hotels/{city}"
    )
    res = requests.get(url=url)
    return res.json()


@mcp.tool()
def book_hotel(
    offer_id: str,
    check_in: str,
    check_out: str,
    name: str,
    rooms_requirement: int,
    adults: int,
):
    """
    Book a hotel.
    Args:
        offer_id (str): Hotel offer ID.
        check_in (str): Check-in date (YYYY-MM-DD).
        check_out (str): Check-out date (YYYY-MM-DD).
        name (str): Name of person, booking the hotel.
        rooms_requirement (int): Number of rooms.
        adults (int): Number of adults.
    """
    payload = {
        "offer_id": offer_id,
        "check_in": check_in,
        "check_out": check_out,
        "name": name,
        "rooms_requirement": rooms_requirement,
        "adults": adults,
    }
    url = "http://localhost:3000/hotels/book"
    res = requests.post(url=url, data=payload)
    return res.json()


@mcp.tool()
def search_flight(departure_city: str, arrival_city: str, departure_date: str):
    """
    Search flights for a given route and date.
    Args:
        departure_city (str): IATA Departure city code.
        arrival_city (str): IATA Arrival city code.
        departure_date (str): Departure date (YYYY-MM-DD).
    """
    payload = {
        "departure_city": departure_city,
        "arrival_city": arrival_city,
        "departure_date": departure_date,
    }
    url = "http://localhost:3000/flights/search"
    res = requests.post(url=url, data=payload)
    return res.json()


@mcp.tool()
def book_flight(offer_id: str, names: list[str], flight_class: str):
    """
    Book a flight.
    Args:
        offer_id (str): Flight offer ID.
        names (list[str]): Passenger names.
        flight_class (str): Travel class, only from - economy, premium_economy, business, first.
    """
    payload = {
        "offer_id": offer_id,
        "names": names,
        "flight_class": flight_class,
    }
    url = "http://localhost:3000/flights/book"
    res = requests.post(url=url, data=payload)
    return res.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
