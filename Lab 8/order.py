from order_line import OrderLine
from product import Product


class Order:
    """Composed of OrderLine objects. The Order creates and manages its own lines;
    lines are never passed in from outside and never moved to another Order."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def __find_order_line(self, product_id: str) -> OrderLine | None:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                return order_line
        return None

    def add_order_line(self, product: Product, quantity: int) -> bool:
        """The Order creates the OrderLine itself (one line per product).
        Adding a product that is already in the order increases its quantity."""
        if quantity < 1:
            return False
        existing = self.__find_order_line(product.get_product_id())
        if existing is not None:
            return existing.update_quantity(existing.get_quantity() + quantity)
        self.__order_lines.append(OrderLine(product, quantity))
        return True

    def update_order_line_quantity(self, product_id: str, quantity: int) -> bool:
        order_line = self.__find_order_line(product_id)
        if order_line is None:
            return False
        return order_line.update_quantity(quantity)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product."""
        order_line = self.__find_order_line(product_id)
        if order_line is None:
            return False
        self.__order_lines.remove(order_line)
        return True

    def get_order_lines(self) -> list[OrderLine]:
        """A copy of the list, so outside code cannot add or take away lines."""
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)
        if not self.__order_lines:
            print("    (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 48)
        print(f"Order Total: ${self.calculate_total():.2f}")