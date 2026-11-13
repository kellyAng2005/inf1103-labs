"""Loads products from a CSV file using try / except / else / finally."""

import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

EXPECTED_COLUMNS: int = 5


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    if len(row) != EXPECTED_COLUMNS:
                        raise ValueError(f"expected {EXPECTED_COLUMNS} columns, got {len(row)}")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type.strip(), product_id.strip(), name.strip(),
                        float(price), int(stock), supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Row {line_number} skipped: ID {product_id.strip()} already exists.")
                except ValueError as error:
                    print(f"Row {line_number} skipped: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")