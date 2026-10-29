import json
import os


# ---------------------------------------------------------------------------
# Product class
# ---------------------------------------------------------------------------
class Product:
    """Represents and manages a single product."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Read-only access for the rest of the program
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Product decides what a valid stock value is."""
        if quantity < 0:
            print("\nStock cannot be negative. Stock not updated.")
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self):
        """Product details needed when saving to JSON."""
        return {"name": self.__name, "price": self.__price, "stock": self.__stock}