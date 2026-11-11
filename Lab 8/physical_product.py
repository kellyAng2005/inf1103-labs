from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. Adds a weight in kilograms."""

    BASE_SHIPPING_FEE: float = 5.00   # flat fee for every shipment
    COST_PER_KG: float = 2.00         # extra cost for each kilogram

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping to the customer."

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING_FEE + self.COST_PER_KG * self.__weight

    def to_dict(self) -> dict[str, str | int | float]:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
