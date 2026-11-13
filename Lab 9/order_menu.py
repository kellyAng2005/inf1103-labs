"""Order menu: Create, Read, Update and Delete orders and their order lines."""

from inventory import Inventory
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount
from input_helpers import get_positive_float


def orders_using_product(orders: dict[str, Order], product_id: str) -> list[str]:
    """IDs of the orders that contain a line for this product."""
    return [
        order_id for order_id, order in orders.items()
        if any(line.get_product().get_product_id() == product_id
               for line in order.get_order_lines())
    ]


def ask_quantity(prompt: str) -> int | None:
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Invalid quantity.")
        return None


def add_line(order: Order, inventory: Inventory) -> None:
    """Ask for a product and quantity, then let the Order create the line."""
    product_id = input("Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    quantity = ask_quantity("Quantity: ")
    if quantity is None:
        return
    try:
        order.add_order_line(product, quantity)
    except ValueError as error:
        print(error)
        return
    print(f"Added {quantity} x {product.get_name()} to order {order.get_order_id()}.")


def create_order(inventory: Inventory, orders: dict[str, Order]) -> None:
    order_id = input("Order ID: ").strip()
    if not order_id:
        print("\nOrder ID cannot be empty. Order not created.")
        return
    if order_id in orders:
        print(f"\nAn order with ID {order_id} already exists.")
        return

    order = Order(order_id)
    while True:
        answer = input("Add a line? (y/n): ").strip().lower()
        if answer != "y":
            break
        add_line(order, inventory)

    if not order.get_order_lines():
        print("\nOrder has no lines. Order not created.")
        return
    orders[order_id] = order
    print("\nOrder created successfully!")
    order.display_information()


def view_all_orders(orders: dict[str, Order]) -> None:
    print("\nAll Orders")
    if not orders:
        print("-" * 48)
        print("No orders.")
        print("-" * 48)
    for order in orders.values():
        order.display_information()


def find_order(orders: dict[str, Order]) -> Order | None:
    order_id = input("Enter Order ID: ").strip()
    order = orders.get(order_id)
    if order is None:
        print("\nOrder not found.")
    return order


def view_order(orders: dict[str, Order]) -> None:
    order = find_order(orders)
    if order is not None:
        order.display_information()


def add_order_line(inventory: Inventory, orders: dict[str, Order]) -> None:
    order = find_order(orders)
    if order is not None:
        add_line(order, inventory)


def update_order_line(orders: dict[str, Order]) -> None:
    order = find_order(orders)
    if order is None:
        return
    order.display_information()
    product_id = input("Product ID of the line to update: ").strip()
    quantity = ask_quantity("New Quantity: ")
    if quantity is None:
        return
    try:
        found = order.update_order_line_quantity(product_id, quantity)
    except ValueError as error:
        print(f"\n{error}")
        return
    if found:
        print("\nOrder line updated successfully!")
    else:
        print("\nOrder line not found.")


def remove_order_line(orders: dict[str, Order]) -> None:
    order = find_order(orders)
    if order is None:
        return
    order.display_information()
    product_id = input("Product ID of the line to remove: ").strip()
    if order.remove_order_line(product_id):
        print("\nOrder line removed successfully!")
    else:
        print("\nOrder line not found.")


def delete_order(orders: dict[str, Order]) -> None:
    order_id = input("Enter Order ID to delete: ").strip()
    if order_id not in orders:
        print("\nOrder not found.")
        return
    del orders[order_id]
    print("\nOrder deleted. Its order lines were removed with it; the products still exist.")


def choose_discount() -> DiscountStrategy | None:
    """Ask which discount to use and build that strategy object."""
    print("\nDiscount type:")
    print("1. No discount")
    print("2. Percentage discount")
    print("3. Bulk discount (amount off when the total reaches a threshold)")
    print("4. Student discount (5%)")
    choice = input("Choose discount (1-4): ").strip()
    try:
        if choice == "1":
            return NoDiscount()
        if choice == "2":
            return PercentageDiscount(get_positive_float("Percentage off (e.g. 10): "))
        if choice == "3":
            threshold = get_positive_float("Threshold total (e.g. 200): ")
            amount = get_positive_float("Amount off (e.g. 20): ")
            return BulkDiscount(threshold, amount)
        if choice == "4":
            return StudentDiscount()
    except ValueError as error:
        print(f"\n{error}")
        return None
    print("\nInvalid discount option.")
    return None


def set_order_discount(orders: dict[str, Order]) -> None:
    order = find_order(orders)
    if order is None:
        return
    discount = choose_discount()
    if discount is None:
        return
    order.set_discount(discount)
    print("\nDiscount updated. Discounts are not saved to inventory.json.")
    order.display_information()


def print_order_menu() -> None:
    print("\n---------- ORDER MENU ----------")
    print("1. Create Order")
    print("2. View All Orders")
    print("3. View One Order")
    print("4. Add Order Line")
    print("5. Update Order Line Quantity")
    print("6. Remove Order Line")
    print("7. Delete Order")
    print("8. Set Order Discount")
    print("9. Back to Main Menu")
    print("--------------------------------")


def order_menu(inventory: Inventory, orders: dict[str, Order]) -> None:
    while True:
        print_order_menu()
        choice = input("\nEnter option: ").strip()
        if choice == "1":
            create_order(inventory, orders)
        elif choice == "2":
            view_all_orders(orders)
        elif choice == "3":
            view_order(orders)
        elif choice == "4":
            add_order_line(inventory, orders)
        elif choice == "5":
            update_order_line(orders)
        elif choice == "6":
            remove_order_line(orders)
        elif choice == "7":
            delete_order(orders)
        elif choice == "8":
            set_order_discount(orders)
        elif choice == "9":
            break
        else:
            print("\nInvalid option. Please try again.")