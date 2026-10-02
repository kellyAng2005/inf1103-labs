"""
INF1103 - Lab 5: Data Manipulation
Inventory Management System

Stores inventory as a dictionary keyed by Product ID, persists it to
data/inventory.json, and exposes CRUD-style operations through a menu.
"""

import json
import os

# Keep the data file in its own folder so a Docker volume can be mounted
# onto just this folder (see Dockerfile) without hiding the app code.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

# Used only the very first time the program runs and no inventory.json
# exists yet - satisfies "store at least three products in a list".
DEFAULT_INVENTORY = {
    "P001": {"name": "Laptop", "price": 1200.00, "stock": 15},
    "P002": {"name": "Mouse", "price": 25.50, "stock": 40},
    "P003": {"name": "Keyboard", "price": 45.00, "stock": 25},
}


# ---------------------------------------------------------------------------
# Data persistence
# ---------------------------------------------------------------------------
def load_inventory():
    """Load inventory.json if it exists, otherwise start from defaults."""
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
            print("Inventory loaded successfully.\n")
            return data
        except (json.JSONDecodeError, OSError):
            print("inventory.json could not be read. Starting with default inventory.\n")
            return dict(DEFAULT_INVENTORY)
    else:
        print(f"{INVENTORY_FILE} not found. Starting with default inventory.\n")
        return dict(DEFAULT_INVENTORY)


def save_inventory(inventory):
    """Write the current inventory dictionary to inventory.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)


# ---------------------------------------------------------------------------
# CRUD operations on the inventory dictionary
# ---------------------------------------------------------------------------
def add_product(inventory):
    """Create: add a new product to the inventory."""
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty. Product not added.")
        return
    if product_id in inventory:
        print(f"\nA product with ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("\nPrice must be a number and stock must be a whole number. Product not added.")
        return

    inventory[product_id] = {"name": name, "price": price, "stock": stock}
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Update: change the stock quantity of an existing product."""
    product_id = input("Enter Product ID: ").strip()
    product = inventory.get(product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    try:
        new_stock = int(input("\nNew Stock Quantity: ").strip())
    except ValueError:
        print("\nInvalid quantity. Stock not updated.")
        return

    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product(inventory):
    """Read: find and display a single product by ID."""
    product_id = input("Enter Product ID: ").strip()
    product = inventory.get(product_id)
    if not product:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product_id}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def display_all(inventory):
    """Read: list every product currently in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    else:
        for product_id, product in inventory.items():
            print(
                f"ID: {product_id} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
            )
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
            display_all(inventory)
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