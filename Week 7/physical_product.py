from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. Adds a weight in kilograms."""

    BASE_SHIPPING_FEE = 5.00   # flat fee for every shipment
    COST_PER_KG = 2.00         # extra cost for each kilogram

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "Requires physical shipping to the customer."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_FEE + self.COST_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data