class StaticLocation:
    def __init__(self, _longitude, _latitude):
        self.longitude = _longitude
        self.latitude = _latitude

class DynamicLocation:
    def __init__(self, _minimum_order, _base_price, _distance_ranges):
        self.minimum_order = _minimum_order
        self.base_price = _base_price
        self.distance_ranges = _distance_ranges

class Data:
    def __str__(self):
        ret = "Data:\n"
        ret += f"longitude: {self.static.longitude}\n"
        ret += f"latitude: {self.static.latitude}\n"
        return ret

    def __init__(self, _longitude, _latitude):
        self.static = StaticLocation(_longitude, _latitude)

    # def initDynamic(self, _minimum_order, _base_price, _distance_ranges):
    #     self.dynamic_loc : DynamicLocation = DynamicLocation

        
