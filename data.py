import time
import requests
import logging
from typing import  Dict 
from enum import Enum


#CUSTOM MODULES
from const import STATIC_LOCATIONS, BASE_URL, ORDER_MIN, BASE_PRICE, DISTANCE_RANGES

class StaticLocation:
    def __str__(self):
        return f"Static data:\n{str(self.locations)}"

    def __init__(self):
        self.locations: Dict[str, Dict[str, float]] = {}
        for _url in STATIC_LOCATIONS:
            try:
                resp_static: requests.Response = requests.get(url=_url)
                if resp_static.status_code != 200:
                    logging.critical(f"Error requesting static API at {_url}. Status code: {resp_static.status_code}, Reason: {resp_static.reason}")
                    continue
                venue_name = _url.split("/")[-2]
                static_data = resp_static.json()
                coordinates = static_data["venue_raw"]["location"]["coordinates"]
                self.set(venue_name, coordinates[0], coordinates[1])
            except Exception as e:
                logging.critical(f"Request failed for {_url}: {e}")

    def set(self, venue_name: str, longitude: float, latitude: float):
        if venue_name not in self.locations:
            self.locations[venue_name] = {}
        coordinates = [longitude, latitude]
        self.locations[venue_name] = coordinates

    async def get_coordinates(self, venue_name: str) -> Dict[str, float]:
        if self.locations.get(venue_name):
            raise Exception(f"Static Location not found in cache: {venue_name}")
        return self.locations[venue_name]

class DynamicLocation:

    @staticmethod
    async def get(venue_name) -> Dict:
        """
        Fetch and parse dynamic data.
        """
        resp = await self.fetch(venue_name)
            
        dynamic_data = resp.json()
        delivery_specs = dynamic_data["venue_raw"]["delivery_specs"]
        delivery_pricing = delivery_specs["delivery_pricing"]
        
        ret: Dict = {}
        ret[ORDER_MIN] = delivery_specs[ORDER_MIN] # int
        ret[BASE_PRICE] = delivery_pricing[BASE_PRICE] # int
        ret[DISTANCE_RANGES] = delivery_pricing[DISTANCE_RANGES]
        ''' "distance_ranges":[{"min":0,"max":500,"a":0,"b":0.0,"flag":null},{"min":500,"max":1000,"a":100,"b":0.0,"flag":null},
        {"min":1000,"max":1500,"a":200,"b":0.0,"flag":null},{"min":1500,"max":2000,"a":200,"b":1.0,"flag":null},{"min":2000,"max":0,"a":0,"b":0.0,"flag":null}] '''
        return ret
            
    @staticmethod
    async def fetch(venue_name: str) -> Dict:
        """
        Fetch dynamic data from the Wolt venue API.
        """
        logging.info(f"Fetching dynamic location: {venue_name}")
        _url = f"{BASE_URL}/{venue_name}/dynamic"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(_url) as resp:
                    logging.info(f"Dynamic request status code: {resp.status}")
                    if resp.status != 200:
                        raise Exception(f"Error requesting dynamic API, response: {resp.status}\n{await resp.text()}")
                    return await resp.json()
        except Exception as e:
            raise Exception(f"Failed request to {_url}: {e}")
    

