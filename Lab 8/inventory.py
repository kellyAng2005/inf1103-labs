from product import Product


class Inventory:
    """Aggregates Product objects. Products exist independently of any Inventory:
    adding or removing one only changes the reference, never the Product itself."""

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID is already present."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove the reference only. The Product object is not destroyed."""
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    def get_all_products(self) -> list[Product]:
        return list(self.__products)