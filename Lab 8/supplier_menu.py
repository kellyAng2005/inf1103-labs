"""Supplier menu: Create, Read, Update and Delete suppliers."""

from supplier import Supplier
from product import Product
from inventory import Inventory


def products_of(supplier: Supplier, inventory: Inventory) -> list[Product]:
    """The products in the inventory that this supplier supplies."""
    return [p for p in inventory.get_all_products() if p.get_supplier() is supplier]


def create_supplier_with_id(supplier_id: str,
                            suppliers: dict[str, Supplier]) -> Supplier | None:
    """Ask for name and email, then create and register the Supplier."""
    name = input("Supplier Name: ").strip()
    email = input("Supplier Contact Email: ").strip()
    if not Supplier.is_valid(name, email):
        print("\nName cannot be empty and the email must contain '@'. Supplier not created.")
        return None
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    """Used by Add Product: pick an existing supplier by ID, or create a new one."""
    print("\nAvailable suppliers:")
    for supplier in suppliers.values():
        print(f"  {supplier.get_supplier_id()} - {supplier.get_name()}")
    supplier_id = input("Supplier ID (existing, or a new ID to create one): ").strip()
    if not supplier_id:
        print("\nSupplier ID cannot be empty. Product not added.")
        return None
    if supplier_id in suppliers:
        return suppliers[supplier_id]
    new_supplier = create_supplier_with_id(supplier_id, suppliers)
    if new_supplier is None:
        print("Product not added.")
    else:
        print(f"New supplier {supplier_id} created.")
    return new_supplier


def create_supplier(suppliers: dict[str, Supplier]) -> None:
    supplier_id = input("Supplier ID: ").strip()
    if not supplier_id:
        print("\nSupplier ID cannot be empty. Supplier not created.")
        return
    if supplier_id in suppliers:
        print(f"\nA supplier with ID {supplier_id} already exists.")
        return
    if create_supplier_with_id(supplier_id, suppliers) is not None:
        print("\nSupplier created successfully!")


def view_all_suppliers(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAll Suppliers")
    print("-" * 48)
    if not suppliers:
        print("No suppliers.")
    for supplier in suppliers.values():
        supplier.display_information()
        print(f"    Products supplied: {len(products_of(supplier, inventory))}")
    print("-" * 48)


def view_supplier(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    supplier_id = input("Enter Supplier ID: ").strip()
    supplier = suppliers.get(supplier_id)
    if supplier is None:
        print("\nSupplier not found.")
        return
    print("\nSupplier Found")
    print("-" * 48)
    supplier.display_information()
    supplied = products_of(supplier, inventory)
    if not supplied:
        print("    No products supplied.")
    for product in supplied:
        print(f"    Supplies: {product.get_product_id()} - {product.get_name()}")
    print("-" * 48)


def update_supplier(suppliers: dict[str, Supplier]) -> None:
    supplier_id = input("Enter Supplier ID: ").strip()
    supplier = suppliers.get(supplier_id)
    if supplier is None:
        print("\nSupplier not found.")
        return
    print("\nSupplier Found:")
    supplier.display_information()
    print("(Press Enter to keep the current value.)")
    name = input("New Name: ").strip() or supplier.get_name()
    email = input("New Contact Email: ").strip() or supplier.get_contact_email()
    if supplier.update_details(name, email):
        print("\nSupplier updated successfully!")


def delete_supplier(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    supplier_id = input("Enter Supplier ID to delete: ").strip()
    supplier = suppliers.get(supplier_id)
    if supplier is None:
        print("\nSupplier not found.")
        return
    supplied = products_of(supplier, inventory)
    if supplied:
        print(f"\nCannot delete: {len(supplied)} product(s) still use this supplier.")
        return
    del suppliers[supplier_id]
    print("\nSupplier deleted successfully!")


def print_supplier_menu() -> None:
    print("\n--------- SUPPLIER MENU ---------")
    print("1. Create Supplier")
    print("2. View All Suppliers")
    print("3. View One Supplier")
    print("4. Update Supplier")
    print("5. Delete Supplier")
    print("6. Back to Main Menu")
    print("---------------------------------")


def supplier_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    while True:
        print_supplier_menu()
        choice = input("\nEnter option: ").strip()
        if choice == "1":
            create_supplier(suppliers)
        elif choice == "2":
            view_all_suppliers(inventory, suppliers)
        elif choice == "3":
            view_supplier(inventory, suppliers)
        elif choice == "4":
            update_supplier(suppliers)
        elif choice == "5":
            delete_supplier(inventory, suppliers)
        elif choice == "6":
            break
        else:
            print("\nInvalid option. Please try again.")