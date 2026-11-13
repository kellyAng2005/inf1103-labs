from discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        if not 0 < percentage <= 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)