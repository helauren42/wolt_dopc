# curl http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087

import requests
import json
import sys

from data import Data

def main():
    resp_static: requests.Response = requests.get(url="https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-berlin/static")

    if resp_static.status_code != 200:
        print("Error requesting static api, response: ", resp_static.status_code)
        print(resp_static.reason)
        sys.exit(1)

    static_data = resp_static.json()
    coordinates = static_data["venue_raw"]["location"]["coordinates"]
    data: Data = Data(coordinates[0], coordinates[1])

    print(data)

if __name__ == "__main__":
    main()