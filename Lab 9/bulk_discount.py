from discount_strategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above the threshold,
    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0 or amount <= 0:
            raise ValueError("Threshold and amount must be greater than zero.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total