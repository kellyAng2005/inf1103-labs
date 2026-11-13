"""Demo for Section 5.2: loads products.csv into an empty Inventory."""

from supplier import Supplier
from inventory import Inventory
from product_loader import load_products

supplier = Supplier("S001", "Demo Supplier", "demo@example.com")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
inventory.display_all()