from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """Abstract base class. Every product is either physical or digital."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        # Association: Product keeps a reference to a Supplier created elsewhere
        self.__supplier: Supplier = supplier

    # Read-only access for the rest of the program
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> bool:
        """Product decides what a valid stock value is."""
        if quantity < 0:
            print("\nStock cannot be negative. Stock not updated.")
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        """Common information. Subclasses extend this using super()."""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self) -> dict[str, str | int | float]:
        """Common details for saving. Subclasses add their own using super()."""
        return {
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Every product type must explain how it is fulfilled."""
        pass