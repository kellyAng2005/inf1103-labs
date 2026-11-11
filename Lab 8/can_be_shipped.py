from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style ABC: anything that can be shipped must calculate its shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass