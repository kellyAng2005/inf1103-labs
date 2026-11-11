"""
INF1103 - Lab 8: Object-Oriented Relationships Part 2
Inventory Management System
(Association, Aggregation, Composition, Type Hints, LSP and Polymorphism)

Main program: main menu and the product menu actions.
Each class lives in its own file:
    supplier.py, product.py, can_be_shipped.py, physical_product.py,
    digital_product.py, inventory.py, order_line.py, order.py
Other files (functions only):
    file_handler.py, supplier_menu.py, order_menu.py, relationship_tests.py
"""

from supplier import Supplier
from product import Product
from can_be_shipped import CanBeShipped
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from file_handler import load_data, save_data
from supplier_menu import choose_supplier, supplier_menu
from order_menu import order_menu, orders_using_product
from relationship_tests import run_relationship_tests


# ---------------------------------------------------------------------------
# Product menu actions (user input lives here, not inside the classes)
# ---------------------------------------------------------------------------
def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty. Product not added.")
        return
    if inventory.find_product(product_id) is not None:
        print(f"\nA product with ID {product_id} already exists.")
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
        extra = float(input("Weight (kg): " if product_type == "1"
                            else "Download Size (MB): ").strip())
        if extra < 0:
            raise ValueError
    except ValueError:
        print("\nInvalid number entered. Product not added.")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        return

    product: Product
    if product_type == "1":
        product = PhysicalProduct(product_id, name, price, stock, supplier, extra)
    else:
        product = DigitalProduct(product_id, name, price, stock, supplier, extra)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
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


def search_product(inventory: Inventory) -> None:
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("    ", end="")
    product.get_supplier().display_information()
    print("-" * 48)


def remove_product(inventory: Inventory, orders: dict[str, Order]) -> None:
    product_id = input("Enter Product ID to remove: ").strip()
    using_orders = orders_using_product(orders, product_id)
    if using_orders:
        print(f"\nCannot remove: the product is used in order(s): {', '.join(using_orders)}.")
        return
    if inventory.remove_product(product_id):
        print("\nProduct removed from the inventory.")
        print("(The Product object itself still exists; only the reference was removed.)")
    else:
        print("\nProduct not found.")


# ---------------------------------------------------------------------------
# Menu system
# ---------------------------------------------------------------------------
def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Remove Product")
    print("8. Manage Suppliers")
    print("9. Manage Orders")
    print("10. Run Relationship Tests")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    inventory, suppliers, orders = load_data()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            print("\nAdd New Product")
            add_product(inventory, suppliers)
        elif choice == "3":
            print("\nUpdate Stock")
            update_stock(inventory)
        elif choice == "4":
            print("\nSearch Product")
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_data(inventory, suppliers, orders)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_data(inventory, suppliers, orders)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        elif choice == "7":
            print("\nRemove Product")
            remove_product(inventory, orders)
        elif choice == "8":
            supplier_menu(inventory, suppliers)
        elif choice == "9":
            order_menu(inventory, orders)
        elif choice == "10":
            run_relationship_tests()
        else:
            print("\nInvalid option. Please try again.")

        print()


if __name__ == "__main__":
    main()