import logging

class CustomerInput:
    pass

class Order:
    def __init__(self, _customer_input):
        self.setCustomerInput(_customer_input)

    def setCustomerInput(self, _customer_input: CustomerInput):
        self.customer_input = _customer_input

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
