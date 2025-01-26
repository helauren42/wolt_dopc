# curl http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087

import uvicorn
import requests
import json
import sys
from fastapi import FastAPI, Query, HTTPException
import logging

# CUSTOM MODULES
from data import LocationData
from const import ORDER_MIN, BASE_PRICE, DISTANCE_RANGES

# GLOBALS
app = FastAPI()
location_data: LocationData
logging.basicConfig(
    level=1,
    handlers=[
        logging.FileHandler("logger", mode="w"),
        logging.StreamHandler()
    ]
)

def main():
    try:
        location_data = LocationData()
    except Exception as e:
        pass
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
