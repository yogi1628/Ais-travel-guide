from amadeus import Client, ResponseError
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

load_dotenv()

AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")

"""
Amadeus Hotel Search Implementation (2024)
Complete workflow: Hotel List -> Hotel Search -> Hotel Booking

Prerequisites:
1. pip install amadeus
2. Register at https://developers.amadeus.com/ for API credentials
"""


class AmadeusHotelSearch:
    def __init__(self, client_id: str, client_secret: str, test_mode: bool = True):
        """
        Initialize Amadeus client

        Args:
            client_id: Your Amadeus API key
            client_secret: Your Amadeus API secret
            test_mode: True for test environment, False for production
        """
        self.amadeus = Client(
            client_id=client_id,
            client_secret=client_secret,
            hostname="test" if test_mode else "production",
        )

    def search_hotels_by_city(
        self,
        city_code: str,
        radius: int = 5,
        radius_unit: str = "KM",
        amenities: Optional[List[str]] = None,
        ratings: Optional[List[str]] = None,
        hotel_source: Optional[str] = None,
    ) -> List[Dict]:
        """
        Step 1: Get list of hotels in a city

        Args:
            city_code: IATA city code (e.g., 'PAR' for Paris, 'NYC' for New York)
            radius: Search radius (default: 5)
            radius_unit: 'KM' or 'MILE' (default: 'KM')
            amenities: List of amenities like ['SWIMMING_POOL', 'SPA', 'FITNESS_CENTER', 'RESTAURANT']
            ratings: Hotel star ratings like ['3', '4', '5']
            hotel_source: 'BEDBANK' or 'DIRECTCHAIN' or None for both

        Returns:
            List of hotels with hotelId, name, and location
        """
        try:
            params = {
                "cityCode": city_code,
                "radius": radius,
                "radiusUnit": radius_unit,
            }

            if amenities:
                params["amenities"] = ",".join(amenities)

            if ratings:
                params["ratings"] = ",".join(ratings)

            if hotel_source:
                params["hotelSource"] = hotel_source

            response = self.amadeus.reference_data.locations.hotels.by_city.get(
                **params
            )

            hotels = []
            for hotel in response.data:
                hotels.append(
                    {
                        "hotelId": hotel.get("hotelId"),
                        "name": hotel.get("name"),
                        "iataCode": hotel.get("iataCode"),
                        "address": hotel.get("address", {}),
                        "geoCode": hotel.get("geoCode", {}),
                        "distance": hotel.get("distance", {}),
                    }
                )

            return hotels

        except ResponseError as error:
            print(f"Error searching hotels by city: {error}")
            return []

    def search_hotels_by_geocode(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5,
        radius_unit: str = "KM",
        amenities: Optional[List[str]] = None,
        ratings: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Step 1 (Alternative): Get list of hotels by geographic coordinates

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius (default: 5)
            radius_unit: 'KM' or 'MILE'
            amenities: List of amenities
            ratings: Hotel star ratings

        Returns:
            List of hotels with hotelId, name, and location
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "radiusUnit": radius_unit,
            }

            if amenities:
                params["amenities"] = ",".join(amenities)

            if ratings:
                params["ratings"] = ",".join(ratings)

            response = self.amadeus.reference_data.locations.hotels.by_geocode.get(
                **params
            )

            hotels = []
            for hotel in response.data:
                hotels.append(
                    {
                        "hotelId": hotel.get("hotelId"),
                        "name": hotel.get("name"),
                        "iataCode": hotel.get("iataCode"),
                        "address": hotel.get("address", {}),
                        "geoCode": hotel.get("geoCode", {}),
                        "distance": hotel.get("distance", {}),
                    }
                )

            return hotels

        except ResponseError as error:
            print(f"Error searching hotels by geocode: {error}")
            return []

    def search_hotel_offers(
        self,
        hotel_ids: List[str],
        check_in_date: str,
        check_out_date: str,
        adults: int = 1,
        room_quantity: int = 1,
        currency: str = "USD",
        payment_policy: str = "NONE",
        board_type: Optional[str] = None,
    ) -> List[Dict]:
        """
        Step 2: Get available offers for specific hotels with real-time pricing

        Args:
            hotel_ids: List of Amadeus hotel IDs (max 3 per request)
            check_in_date: Check-in date in YYYY-MM-DD format (must be future date)
            check_out_date: Check-out date in YYYY-MM-DD format
            adults: Number of adult guests per room (1-9)
            room_quantity: Number of rooms (1-9)
            currency: Currency code (e.g., 'USD', 'EUR', 'GBP', 'INR')
            payment_policy: 'NONE', 'GUARANTEE', 'DEPOSIT'
            board_type: Meal plan - 'ROOM_ONLY', 'BREAKFAST', 'HALF_BOARD', 'FULL_BOARD'

        Returns:
            List of hotel offers with pricing and room details
        """
        try:
            # Build parameters
            params = {
                "hotelIds": (
                    hotel_ids if isinstance(hotel_ids, str) else ",".join(hotel_ids[:3])
                ),
                "checkInDate": check_in_date,
                "checkOutDate": check_out_date,
                "adults": adults,
                "roomQuantity": room_quantity,
                "currency": currency,
                "paymentPolicy": payment_policy,
            }

            if board_type:
                params["boardType"] = board_type

            print(f"Searching with params: {params}")

            # Use the correct endpoint - shopping.hotel_offers_search (note the 's' in offers)
            response = self.amadeus.shopping.hotel_offers_search.get(**params)

            # Check if response.data exists and is not None
            if not hasattr(response, "data") or response.data is None:
                print("No data in response")
                return []

            offers = []
            for hotel_offer in response.data:
                hotel_info = {
                    "hotelId": hotel_offer.get("hotel", {}).get("hotelId"),
                    "name": hotel_offer.get("hotel", {}).get("name"),
                    "rating": hotel_offer.get("hotel", {}).get("rating"),
                    "cityCode": hotel_offer.get("hotel", {}).get("cityCode"),
                    "latitude": hotel_offer.get("hotel", {}).get("latitude"),
                    "longitude": hotel_offer.get("hotel", {}).get("longitude"),
                    "offers": [],
                }

                for offer in hotel_offer.get("offers", []):
                    offer_details = {
                        "offerId": offer.get("id"),
                        "checkInDate": offer.get("checkInDate"),
                        "checkOutDate": offer.get("checkOutDate"),
                        "roomType": offer.get("room", {}).get("type"),
                        "roomDescription": offer.get("room", {})
                        .get("description", {})
                        .get("text"),
                        "beds": offer.get("room", {})
                        .get("typeEstimated", {})
                        .get("beds"),
                        "bedType": offer.get("room", {})
                        .get("typeEstimated", {})
                        .get("bedType"),
                        "guests": offer.get("guests", {}).get("adults"),
                        "price": {
                            "currency": offer.get("price", {}).get("currency"),
                            "total": offer.get("price", {}).get("total"),
                            "base": offer.get("price", {}).get("base"),
                            "taxes": offer.get("price", {}).get("taxes", []),
                        },
                        "policies": {
                            "cancellation": offer.get("policies", {}).get(
                                "cancellation"
                            ),
                            "paymentType": offer.get("policies", {}).get("paymentType"),
                            "guarantee": offer.get("policies", {}).get("guarantee"),
                        },
                        "boardType": offer.get("boardType"),
                        "self_link": offer.get("self"),
                    }
                    hotel_info["offers"].append(offer_details)

                offers.append(hotel_info)

            return offers

        except ResponseError as error:
            print(f"Error searching hotel offers: {error}")
            print(
                f"Error details: {error.response.body if hasattr(error, 'response') else 'No details'}"
            )
            return []

    def get_hotel_offer_details(self, offer_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific hotel offer

        Args:
            offer_id: The offer ID from search results

        Returns:
            Detailed offer information
        """
        try:
            response = self.amadeus.shopping.hotel_offer_search(offer_id).get()
            return response.data

        except ResponseError as error:
            print(f"Error getting offer details: {error}")
            print(
                f"Error details: {error.response.body if hasattr(error, 'response') else 'No details'}"
            )
            return None

    def search_hotel_by_name(
        self,
        keyword: str,
        subtype: str = "HOTEL_LEISURE",
        country_code: Optional[str] = None,
        max_results: int = 20,
    ) -> List[Dict]:
        """
        Search hotels by name/keyword (autocomplete functionality)

        Args:
            keyword: Search keyword (4-40 characters)
            subtype: 'HOTEL_LEISURE' for aggregators or 'HOTEL_GDS' for chains
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'FR')
            max_results: Maximum number of results (1-20)

        Returns:
            List of matching hotels
        """
        try:
            params = {"keyword": keyword, "subType": subtype, "max": max_results}

            if country_code:
                params["countryCode"] = country_code

            response = self.amadeus.reference_data.locations.hotels.by_hotels.get(
                **params
            )

            hotels = []
            for hotel in response.data:
                hotels.append(
                    {
                        "hotelId": hotel.get("hotelId"),
                        "name": hotel.get("name"),
                        "iataCode": hotel.get("iataCode"),
                        "address": hotel.get("address", {}),
                        "geoCode": hotel.get("geoCode", {}),
                    }
                )

            return hotels

        except ResponseError as error:
            print(f"Error searching hotels by name: {error}")
            return []


hotel_search = AmadeusHotelSearch(
    client_id=AMADEUS_CLIENT_ID, client_secret=AMADEUS_CLIENT_SECRET, test_mode=True
)
