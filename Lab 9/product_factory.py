from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Factory pattern: the one place that knows which Product class to create.
    Creates products but does not store them (a dependency, not an association)."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, extra: float = 0.0) -> Product:
        """extra is the weight (kg) for a physical product, or the download size (MB)
        for a digital product."""
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra)
        else:
            raise ValueError(f"Unknown product type: {product_type}")