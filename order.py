import logging

class CustomerInput:
    pass

class Order:
    def __init__(self, _customer_input):
        self.setCustomerInput(_customer_input)

    def setCustomerInput(self, _customer_input: CustomerInput):
        self.customer_input = _customer_input

    def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """
        Calculate the great distance two coordinates.
        """
        lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        radius_km = 6371
        return c * radius_km

    def setResult(self, _total_price, _small_order_surcharge, _cart_value, _fee, _distance):
        self.total_price = _total_price
        self.small_order_surcharge = _small_order_surcharge
        self.cart_value = _cart_value
        # delivery
        self.fee = _fee
        self.distance = _distance

    def getResult(self) -> dict:
        result = {
            "total_price": self.total_price,
            "small_order_surcharge": self.small_order_surcharge,
            "cart_value": self.cart_value,
            "delivery": {
                "fee": self.fee,
                "distance": self.distance,
            }
        }
        return result
