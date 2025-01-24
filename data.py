import time
import requests

class StaticLocation:
    def __init__(self):
        resp_static: requests.Response = requests.get(url="https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-berlin/static")
        if resp_static.status_code != 200:
            logging.warning("Error requesting static api, response: ", resp_static.status_code)
            logging.warning(resp_static.reason)
        static_data = resp_static.json()
        coordinates = static_data["venue_raw"]["location"]["coordinates"]
        self.set(coordinates[0], coordinates[1])

    def set(self, _longitude, _latitude):
        self.longitude = _longitude
        self.latitude = _latitude

class DynamicLocation:
    def __init__(self):
        self.fetchAndSet()
    
    def fetchAndSet(self):
        resp: requests.Response = requests.get(url="https://conswumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-berlin/dynamic")
        if resp.status_code != 200:
            logging.critical("Error requesting static api, response: ", resp_static.status_code)
            logging.critical(resp_static.reason)
            return
        dynamic_data = resp.json()
        delivery_specs = dynamic_data["venue_raw"]["delivery_specs"]
        delivery_pricing = delivery_specs["delivery_pricing"]
        self.set(delivery_specs["order_minimum_no_surcharge"], delivery_pricing["base_price"], delivery_pricing["distance_ranges"])

    def set(self, _order_minimum_no_surcharge, _base_price, _distance_ranges):
        self.order_minimum_no_surcharge = _order_minimum_no_surcharge
        self.base_price = _base_price
        self.distance_ranges: List[Dict[str:int]] = _distance_ranges

        ''' "distance_ranges":[{"min":0,"max":500,"a":0,"b":0.0,"flag":null},{"min":500,"max":1000,"a":100,"b":0.0,"flag":null},
        {"min":1000,"max":1500,"a":200,"b":0.0,"flag":null},{"min":1500,"max":2000,"a":200,"b":1.0,"flag":null},{"min":2000,"max":0,"a":0,"b":0.0,"flag":null}] '''

class Data:
    def __str__(self):
        ret = "Static data:\n"
        ret += f"longitude: {self.static.longitude}\n"
        ret += f"latitude: {self.static.latitude}\n"
        ret += "Dynamic data:\n"
        ret += f"order_minimum_no_surcharge: {self.dynamic.order_minimum_no_surcharge}\n"
        ret += f"base_price: {self.dynamic.base_price}\n"
        ret += f"distance_ranges: {self.dynamic.distance_ranges}\n"
        return ret

    def __init__(self):
        self.static = StaticLocation()
        self.last_dynamic_init = 0
        self.dynamicInit()

    def dynamicInit(self):
        now = time.time()
        if self.last_dynamic_init > now - 15:
            return
        self.last_dynamic_init = now
        self.dynamic = DynamicLocation()
    
    # def initDynamic(self, _order_minimum_no_surcharge, _base_price, _distance_ranges):
    #     self.dynamic_loc : DynamicLocation = DynamicLocation
