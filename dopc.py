import uvicorn
import requests
import json
import sys
from fastapi import FastAPI, Query, HTTPException
import logging
from math import radians, sin, cos, asin, sqrt

# CUSTOM MODULES
from data import static_data, DynamicLocation
from const import ORDER_MIN, BASE_PRICE, DISTANCE_RANGES

# GLOBALS
app = FastAPI()
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("logger.log", mode="w"),
        logging.StreamHandler()
    ]
)

class CustomerInput:
    def __init__(self, _venue_slug: str, _cart_value: int, _lon: float, _lat: float):
        self.venue_slug = _venue_slug
        self.cart_value = _cart_value
        self.lon = _lon
        self.lat = _lat

class Order:

    @staticmethod
    def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """
        Get the distance between two coordinates.
        """
        lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        radius_km = 6371
        logging.debug(f"Calculated haversine distance: {c * radius_km} km")
        return c * radius_km * 1000

    @staticmethod
    def calculatePrice(customer_input: CustomerInput, dynamic_data: DynamicLocation, delivery_distance: float) -> dict:
        logging.debug(f"Calculating price for venue: {customer_input.venue_slug}, cart value: {customer_input.cart_value}, distance: {delivery_distance} km")
        distance_ranges = dynamic_data[DISTANCE_RANGES]
        order_minimum_no_surcharge = dynamic_data[ORDER_MIN]
        
        # calculate delivery fee
        delivery_fee = dynamic_data[BASE_PRICE]
        logging.debug(f"Base delivery fee: {delivery_fee}")

        for range in distance_ranges:
            if range["max"] == 0 and delivery_distance >= range["min"]:
                raise Exception(f"Delivery not possible for this distance {delivery_distance}")
            if range["min"] <= delivery_distance < range["max"]:
                delivery_fee += range["a"] + round(range["b"] * delivery_distance / 10)
                logging.debug(f"Updated delivery fee: {delivery_fee}")
                break
        else:
            raise Exception(f"Delivery not possible for this distance {delivery_distance}")

        small_order_surcharge = max(0, order_minimum_no_surcharge - customer_input.cart_value)
        total_price = customer_input.cart_value + small_order_surcharge + delivery_fee
        logging.debug(f"Total price: {total_price}, Small order surcharge: {small_order_surcharge}")

        result = {
            "total_price": total_price,
            "small_order_surcharge": small_order_surcharge,
            "cart_value": customer_input.cart_value,
            "delivery": {
                "fee": delivery_fee,
                "distance": delivery_distance,
            }
        }
        return result

@app.get("/api/v1/delivery-order-price")
async def get_delivery_order_price(
    venue_slug: str = Query(..., description="The unique identifier for the venue"),
    cart_value: int = Query(..., description="The shopping cart total value"),
    user_lat: float = Query(..., description="The latitude of the user's location"),
    user_lon: float = Query(..., description="The longitude of the user's location"),
    ):
    logging.info(f"Received request to calculate delivery order price for venue: {venue_slug}, cart value: {cart_value}, user location: ({user_lat}, {user_lon})")
    
    customer_input = CustomerInput(venue_slug, cart_value, user_lat, user_lon)
    
    try:
        logging.debug(f"Fetching static data for venue: {venue_slug}")
        venue_coordinates = await static_data.get_coordinates(venue_slug)
        logging.info(f"Venue coordinates for {venue_slug}: {venue_coordinates}")
    except Exception as e:
        logging.critical(f"Error fetching coordinates: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching venue coordinates: {str(e)}")

    try:
        logging.debug(f"Fetching dynamic data for venue: {venue_slug}")
        dynamic_data = await DynamicLocation.get(venue_slug)
        logging.info(f"Dynamic venue data for {venue_slug} fetched successfully")
    except Exception as e:
        logging.critical(f"Error fetching dynamic venue data: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching venue data: {str(e)}")

    try:
        logging.debug("Calculating delivery distance using haversine formula")
        delivery_distance = Order.haversine(user_lon, user_lat, venue_coordinates[0], venue_coordinates[1])
        logging.info(f"Delivery distance: {delivery_distance} km")
        
        logging.debug("Calculating total price")
        result = Order.calculatePrice(customer_input, dynamic_data, delivery_distance)
        logging.info(f"Calculated price successfully: {result['total_price']}")
        return result
    except Exception as e:
        logging.error(f"Error calculating delivery price: {e}")
        raise HTTPException(status_code=422, detail=f"Error calculating delivery price: {str(e)}")

def main():
    logging.info("Starting application")
    if len(static_data.locations) == 0:
        logging.critical("No static locations found")
        raise Exception("No static locations found")

    logging.info("Starting Uvicorn server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
