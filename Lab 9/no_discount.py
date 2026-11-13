from discount_strategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total