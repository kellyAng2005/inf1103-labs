class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = {}  # product_id -> Product

    def add_product(self, product):
        product_id = product.get_product_id()
        if product_id in self.__products:
            return False
        self.__products[product_id] = product
        return True

    def search_product(self, product_id):
        """Return the Product with this ID, or None."""
        return self.__products.get(product_id)

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products.values():
                product.display_information()
        print("-" * 48)

    def get_all_products(self):
        return list(self.__products.values())