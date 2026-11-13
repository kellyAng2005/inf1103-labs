from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    """Composed of OrderLine objects. The Order creates and manages its own lines;
    lines are never passed in from outside and never moved to another Order.

    The Order also USES a DiscountStrategy (association). It does not decide the
    discount itself: it just asks the strategy to apply() it."""

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Change the discount strategy at any time."""
        self.__discount = discount

    def __find_order_line(self, product_id: str) -> OrderLine | None:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                return order_line
        return None

    def add_order_line(self, product: Product, quantity: int) -> None:
        """The Order creates the OrderLine itself (one line per product).
        Adding a product that is already in the order increases its quantity.
        Raises ValueError if the quantity is not greater than zero."""
        existing = self.__find_order_line(product.get_product_id())
        if existing is not None:
            existing.increase_quantity(quantity)
        else:
            self.__order_lines.append(OrderLine(product, quantity))

    def update_order_line_quantity(self, product_id: str, quantity: int) -> bool:
        """Returns False if there is no line for this product.
        Raises ValueError if the quantity is not greater than zero."""
        order_line = self.__find_order_line(product_id)
        if order_line is None:
            return False
        order_line.update_quantity(quantity)
        return True

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

    def calculate_subtotal(self) -> float:
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)

    def calculate_total(self) -> float:
        total = self.calculate_subtotal()
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)
        if not self.__order_lines:
            print("    (no order lines)")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 48)
        print(f"Items Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Order Total (after discount): ${self.calculate_total():.2f}")