from product import Product


class OrderLine:
    """One product and quantity inside an Order.

    Composition: only Order creates OrderLine objects (see Order.add_order_line).
    An OrderLine refers to a Product but does not own it.
    """

    @staticmethod
    def validate_quantity(quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

    def __init__(self, product: Product, quantity: int) -> None:
        OrderLine.validate_quantity(quantity)
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def update_quantity(self, quantity: int) -> None:
        """Raises ValueError if the quantity is not greater than zero."""
        OrderLine.validate_quantity(quantity)
        self.__quantity = quantity

    def increase_quantity(self, amount: int) -> None:
        """Add to the quantity. Raises ValueError if the amount is not greater than zero."""
        OrderLine.validate_quantity(amount)
        self.__quantity += amount

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(
            f"    {self.__product.get_name()} ({self.__product.get_product_id()}) | "
            f"Qty: {self.__quantity} | Unit: ${self.__product.get_price():.2f} | "
            f"Subtotal: ${self.calculate_subtotal():.2f}"
        )