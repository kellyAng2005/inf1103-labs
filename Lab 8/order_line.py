from product import Product


class OrderLine:
    """One product and quantity inside an Order.

    Composition: only Order creates OrderLine objects (see Order.add_order_line).
    An OrderLine refers to a Product but does not own it.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def update_quantity(self, quantity: int) -> bool:
        """OrderLine decides what a valid quantity is."""
        if quantity < 1:
            return False
        self.__quantity = quantity
        return True

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(
            f"    {self.__product.get_name()} ({self.__product.get_product_id()}) | "
            f"Qty: {self.__quantity} | Unit: ${self.__product.get_price():.2f} | "
            f"Subtotal: ${self.calculate_subtotal():.2f}"
        )