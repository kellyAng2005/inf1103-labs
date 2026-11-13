from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: every discount provides the same apply() method."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass