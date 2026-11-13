from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """Fourth strategy: a flat 5% student discount. Order did not need to change."""

    STUDENT_RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.STUDENT_RATE)