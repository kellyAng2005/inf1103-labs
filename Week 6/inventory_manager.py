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

    

# ---------------------------------------------------------------------------
# Inventory class
# ---------------------------------------------------------------------------
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

    

# ---------------------------------------------------------------------------
# File handling (inventory.json sits in the same folder as this file)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")


def default_inventory():
    """Used only if inventory.json is missing or unreadable."""
    inventory = Inventory()
    inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
    inventory.add_product(Product("P002", "Mouse", 25.50, 40))
    inventory.add_product(Product("P003", "Keyboard", 45.00, 25))
    return inventory


def load_inventory():
    """Build an Inventory object from inventory.json."""
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            inventory = Inventory()
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
            for product_id, info in data.items():
                inventory.add_product(
                    Product(product_id, info["name"], info["price"], info["stock"])
                )
            print("Inventory loaded successfully.\n")
            return inventory
        except (json.JSONDecodeError, OSError, KeyError, AttributeError):
            print("inventory.json could not be read. Starting with default inventory.\n")
            return default_inventory()
    print(f"{INVENTORY_FILE} not found. Starting with default inventory.\n")
    return default_inventory()


def save_inventory(inventory):
    """Write every Product in the Inventory to inventory.json."""
    data = {p.get_product_id(): p.to_dict() for p in inventory.get_all_products()}
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------------------------
# Menu actions (user input lives here, not inside the classes)
# ---------------------------------------------------------------------------
def add_product(inventory):
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty. Product not added.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("\nPrice must be a number and stock must be a whole number. Product not added.")
        return

    if inventory.add_product(Product(product_id, name, price, stock)):
        print("\nProduct added successfully!")
    else:
        print(f"\nA product with ID {product_id} already exists.")


def update_stock(inventory):
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    try:
        new_stock = int(input("\nNew Stock Quantity: ").strip())
    except ValueError:
        print("\nInvalid quantity. Stock not updated.")
        return

    if product.update_stock(new_stock):
        print("\nStock updated successfully!")


def search_product(inventory):
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)


# ---------------------------------------------------------------------------
# Menu system
# ---------------------------------------------------------------------------
def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    inventory = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            print("\nAdd New Product")
            add_product(inventory)
        elif choice == "3":
            print("\nUpdate Stock")
            update_stock(inventory)
        elif choice == "4":
            print("\nSearch Product")
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please try again.")

        print()


if __name__ == "__main__":
    main()