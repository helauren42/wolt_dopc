class CustomerInput:
    pass

class Order:
    def __init__(self):
        pass

    def setCustomerInput(self, _customer_input: CustomerInput):
        self.customer_input: CustomerInput = _customer_input

    def setResult(self, _total_price, _small_order_surcharge, _cart_value, _fee, _distance):
        self.total_price: int = _total_price
        self.small_order_surcharge: int = _small_order_surcharge
        self.cart_value: int = _cart_value
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
