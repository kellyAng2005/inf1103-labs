"""
INF1103 - Lab 7: Object-Oriented Relationships Part 1
Inventory Management System (Inheritance, Overriding, Abstract classes, Interfaces)

Main program: menu, user input, loading/saving JSON.
Each class lives in its own file:
    product.py, can_be_shipped.py, physical_product.py,
    digital_product.py, inventory.py
"""

import json
import os

from product import Product
from can_be_shipped import CanBeShipped
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

# inventory.json sits in the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.json")


# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------
def default_inventory():
    """Used only if inventory.json is missing or unreadable."""
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.2))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1))
    inventory.add_product(DigitalProduct("D001", "E-Book", 12.90, 100, 12.5))
    return inventory


def product_from_dict(product_id, info):
    """Use the saved 'type' to create the right Product subclass."""
    product_type = info.get("type", "physical")  # Lab 6 files had no type
    if product_type == "physical":
        return PhysicalProduct(
            product_id, info["name"], info["price"], info["stock"],
            info.get("weight", 0.0),
        )
    if product_type == "digital":
        return DigitalProduct(
            product_id, info["name"], info["price"], info["stock"],
            info["download_size"],
        )
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory():
    """Build an Inventory object from inventory.json."""
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            inventory = Inventory()
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
            for product_id, info in data.items():
                inventory.add_product(product_from_dict(product_id, info))
            print("Inventory loaded successfully.\n")
            return inventory
        except (json.JSONDecodeError, OSError, KeyError, AttributeError, ValueError, TypeError):
            print("inventory.json could not be read. Starting with default inventory.\n")
            return default_inventory()
    print(f"{INVENTORY_FILE} not found. Starting with default inventory.\n")
    return default_inventory()


def save_inventory(inventory):
    """Write every Product (with its type and extra attributes) to inventory.json."""
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

    print("Product Type:")
    print("1. Physical")
    print("2. Digital")
    product_type = input("Choose type (1/2): ").strip()
    if product_type not in ("1", "2"):
        print("\nInvalid product type. Product not added.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
        if product_type == "1":
            weight = float(input("Weight (kg): ").strip())
            if weight < 0:
                raise ValueError
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): ").strip())
            if download_size < 0:
                raise ValueError
            product = DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError:
        print("\nInvalid number entered. Product not added.")
        return

    if inventory.add_product(product):
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
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def run_class_tests():
    """Section 7 checks, run on temporary objects (not added to the inventory)."""
    print("\nRunning class tests...")
    physical = PhysicalProduct("T001", "Test Guitar", 350.00, 5, 3.5)
    digital = DigitalProduct("T002", "Test Software", 99.00, 100, 4200.0)

    print("\n1. Physical product stores and displays its weight:")
    physical.display_information()

    print("\n2. Digital product stores and displays its download size:")
    digital.display_information()

    print("\n3. Both subclasses implement get_fulfilment_info():")
    print(f"   Physical: {physical.get_fulfilment_info()}")
    print(f"   Digital:  {digital.get_fulfilment_info()}")

    print("\n4. Product is abstract and cannot be created directly:")
    try:
        Product("T003", "Generic", 1.00, 1)
    except TypeError as error:
        print(f"   TypeError: {error}")

    print("\n5. Physical products calculate shipping cost:")
    for weight in (0.5, 2, 10):
        item = PhysicalProduct("T004", "Weight Test", 10.00, 1, weight)
        print(f"   {weight} kg -> ${item.calculate_shipping_cost():.2f}")

    print("\n6. Interface check (CanBeShipped):")
    print(f"   Physical can be shipped: {isinstance(physical, CanBeShipped)}")
    print(f"   Digital can be shipped:  {isinstance(digital, CanBeShipped)}")


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
    print("7. Run Class Tests")
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
        elif choice == "7":
            run_class_tests()
        else:
            print("\nInvalid option. Please try again.")

        print()


if __name__ == "__main__":
    main()