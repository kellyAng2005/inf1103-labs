"""
JSON file handling: loads and saves suppliers, products and orders.
inventory.json sits in the same folder as this file.
"""

import json
import os

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from inventory import Inventory
from order import Order

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE: str = os.path.join(BASE_DIR, "inventory.json")
DEFAULT_SUPPLIER_ID: str = "S000"

# A saved product is a dictionary of simple JSON values
JsonInfo = dict[str, str | int | float]
# Everything the program needs: products, suppliers, orders
AppData = tuple[Inventory, dict[str, Supplier], dict[str, Order]]


def default_data() -> AppData:
    """Used only if inventory.json is missing or unreadable."""
    suppliers: dict[str, Supplier] = {
        "S001": Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com"),
        "S002": Supplier("S002", "DigiWorld Pte Ltd", "support@digiworld.example.com"),
    }
    inventory = Inventory()
    inventory.add_product(ProductFactory.create(
        "physical", "P001", "Laptop", 1200.00, 15, suppliers["S001"], 2.2))
    inventory.add_product(ProductFactory.create(
        "physical", "P002", "Mouse", 25.50, 40, suppliers["S001"], 0.1))
    inventory.add_product(ProductFactory.create(
        "digital", "D001", "E-Book", 12.90, 100, suppliers["S002"], 12.5))
    return inventory, suppliers, {}


def product_from_dict(product_id: str, info: JsonInfo,
                      suppliers: dict[str, Supplier]) -> Product:
    """Use the saved 'type' to create the right Product subclass."""
    supplier_id = str(info.get("supplier_id", DEFAULT_SUPPLIER_ID))  # Lab 7 files had none
    if supplier_id not in suppliers:
        if supplier_id != DEFAULT_SUPPLIER_ID:
            raise KeyError(supplier_id)
        suppliers[supplier_id] = Supplier(DEFAULT_SUPPLIER_ID, "Unknown Supplier",
                                          "unknown@example.com")
    supplier: Supplier = suppliers[supplier_id]

    name = str(info["name"])
    price = float(info["price"])
    stock = int(info["stock"])
    product_type = str(info.get("type", "physical"))  # Lab 6 files had no type
    if product_type == "digital":
        extra = float(info["download_size"])
    else:
        extra = float(info.get("weight", 0.0))
    # The factory decides which class to create (and rejects unknown types)
    return ProductFactory.create(product_type, product_id, name, price, stock,
                                 supplier, extra)


def load_data() -> AppData:
    """Build the Inventory, the supplier list and the orders from inventory.json."""
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                data = json.load(f)
            # Lab 7 files were just a dictionary of products
            new_format: bool = "products" in data
            supplier_data: dict[str, dict[str, str]] = data["suppliers"] if new_format else {}
            product_data: dict[str, JsonInfo] = data["products"] if new_format else data
            order_data: dict[str, list[dict[str, str | int]]] = (
                data.get("orders", {}) if new_format else {}
            )

            suppliers: dict[str, Supplier] = {}
            for supplier_id, supplier_info in supplier_data.items():
                suppliers[supplier_id] = Supplier(supplier_id, supplier_info["name"],
                                                  supplier_info["contact_email"])
            inventory = Inventory()
            for product_id, product_info in product_data.items():
                inventory.add_product(product_from_dict(product_id, product_info, suppliers))

            # Orders are rebuilt through Order, which creates its own OrderLines
            orders: dict[str, Order] = {}
            for order_id, lines in order_data.items():
                order = Order(order_id)
                for line in lines:
                    product = inventory.find_product(str(line["product_id"]))
                    if product is None:
                        print(f"Warning: product {line['product_id']} in order "
                              f"{order_id} not found. Line skipped.")
                        continue
                    order.add_order_line(product, int(line["quantity"]))
                orders[order_id] = order

            print("Inventory loaded successfully.\n")
            return inventory, suppliers, orders
        except (json.JSONDecodeError, OSError, KeyError, AttributeError, ValueError, TypeError):
            print("inventory.json could not be read. Starting with default inventory.\n")
            return default_data()
    print(f"{INVENTORY_FILE} not found. Starting with default inventory.\n")
    return default_data()


def save_data(inventory: Inventory, suppliers: dict[str, Supplier],
              orders: dict[str, Order]) -> None:
    """Write suppliers, products and orders (with their lines) to inventory.json."""
    data = {
        "suppliers": {
            supplier_id: {"name": s.get_name(), "contact_email": s.get_contact_email()}
            for supplier_id, s in suppliers.items()
        },
        "products": {
            p.get_product_id(): p.to_dict() for p in inventory.get_all_products()
        },
        "orders": {
            order_id: [
                {"product_id": line.get_product().get_product_id(),
                 "quantity": line.get_quantity()}
                for line in order.get_order_lines()
            ]
            for order_id, order in orders.items()
        },
    }
    try:
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except OSError:
        print("Could not save inventory.json. Check that the folder is writable.")