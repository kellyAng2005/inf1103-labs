"""
Lab 8/9 test functions: association, aggregation, composition, LSP, polymorphism.
Run from the main menu (option 10). All objects here are temporary test data.
"""

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    """Works with ANY Product: uses only behaviour that Product promises."""
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")


def test_association() -> None:
    print("\n=== 1. ASSOCIATION: Supplier and Product ===")
    supplier = Supplier("S900", "Test Supplier Pte Ltd", "test@example.com")
    physical = ProductFactory.create("physical", "T001", "Test Guitar", 350.00, 5, supplier, 3.5)
    digital = ProductFactory.create("digital", "T002", "Test Software", 99.00, 100, supplier, 4200.0)

    print("Supplier information displayed through each Product:")
    physical.get_supplier().display_information()
    digital.get_supplier().display_information()
    print(f"Both products share the same Supplier object: "
          f"{physical.get_supplier() is digital.get_supplier() is supplier}")

    print("\nPredict first check: del supplier, then ask the products again...")
    del supplier
    print("Variable 'supplier' deleted. Products still hold their own references:")
    physical.get_supplier().display_information()
    digital.get_supplier().display_information()


def test_aggregation() -> None:
    print("\n=== 2. AGGREGATION: Inventory and Product ===")
    supplier = Supplier("S901", "Aggregation Supplier", "agg@example.com")
    product = ProductFactory.create("physical", "T003", "Test Mouse", 25.50, 10, supplier, 0.1)
    print("Product created BEFORE any Inventory exists:")
    product.display_information()

    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(product)
    print(f"Added to Inventory A. A contains it: "
          f"{inventory_a.find_product('T003') is product}")

    inventory_a.remove_product("T003")
    print(f"Removed from Inventory A. A contains it: "
          f"{inventory_a.find_product('T003') is not None}")
    print("Product still works after removal:")
    product.update_stock(8)
    product.display_information()

    inventory_b.add_product(product)
    print(f"Added the SAME object to Inventory B. B has the same object: "
          f"{inventory_b.find_product('T003') is product}")
    print(f"Inventory A is now empty ({len(inventory_a.get_all_products())} products) "
          f"but the Product still exists.")


def test_composition() -> None:
    print("\n=== 3. COMPOSITION: Order and OrderLine ===")
    supplier = Supplier("S902", "Order Supplier", "order@example.com")
    guitar = ProductFactory.create("physical", "T004", "Test Guitar", 350.00, 5, supplier, 3.5)
    software = ProductFactory.create("digital", "T005", "Test Software", 99.00, 100, supplier, 4200.0)

    order_1 = Order("O-001")
    order_1.add_order_line(guitar, 2)
    order_1.add_order_line(software, 1)
    order_1.display_information()

    order_2 = Order("O-002")
    order_2.add_order_line(guitar, 1)
    order_2.display_information()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print("\nSame Product in two different Orders:")
    print(f"  Same OrderLine object? {line_1 is line_2}  (each Order created its own)")
    print(f"  Same Product object?   {line_1.get_product() is line_2.get_product()}")
    print("  OrderLine objects: 2, Product objects: 1")

    order_1.remove_order_line("T005")
    print("\nRemoved the software line from Order O-001:")
    order_1.display_information()
    del order_2
    print("\nOrder O-002 deleted (its OrderLine goes with it). The Product still works:")
    guitar.display_information()


def test_lsp_and_polymorphism() -> None:
    print("\n=== 4. LSP AND POLYMORPHISM ===")
    supplier = Supplier("S903", "LSP Supplier", "lsp@example.com")
    physical = ProductFactory.create("physical", "T006", "Test Keyboard", 79.90, 25, supplier, 0.9)
    digital = ProductFactory.create("digital", "T007", "Test E-Book", 12.90, 100, supplier, 12.5)

    print("show_product_details() called with each product type:")
    show_product_details(physical)
    show_product_details(digital)

    print("\nBoth subclasses keep Product's update_stock() promise:")
    for product in (physical, digital):
        product.update_stock(10)
        accepted = product.get_stock() == 10
        try:
            product.update_stock(-1)
            rejected = False
        except ValueError:
            rejected = True
        print(f"  {product.get_name()}: accepts 10 -> {accepted}, rejects -1 -> {rejected}")

    inventory = Inventory()
    inventory.add_product(physical)
    inventory.add_product(digital)
    print("\nOne loop over Product references (no isinstance checks):")
    for item in inventory.get_all_products():
        item.display_information()
        print(f"    Fulfilment: {item.get_fulfilment_info()}")


def run_relationship_tests() -> None:
    print("\nRunning Lab 8 relationship tests...")
    test_association()
    test_aggregation()
    test_composition()
    test_lsp_and_polymorphism()
    print("\nAll relationship tests finished.")