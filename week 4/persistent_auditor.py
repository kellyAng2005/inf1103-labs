ORDERS_FILE = "orders.txt"
STARTING_ID = 1001


def load_orders():
    """Read orders.txt and return a list of orders: [[id, product, qty], ...].
    If the file doesn't exist yet, return an empty list (no crash on first run)."""
    orders = []
    try:
        with open(ORDERS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip blank lines
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    continue  # skip badly formatted lines
                orders.append([int(parts[0]), parts[1], int(parts[2])])
    except FileNotFoundError:
        pass
    return orders


def save_orders(orders):
    """Overwrite orders.txt with every order, one per line: id,product,qty"""
    with open(ORDERS_FILE, "w") as f:
        for order in orders:
            f.write(format_order(order) + "\n")


def format_order(order):
    """Turn [1004, 'Laptop Stand', 2] into '1004,Laptop Stand,2'."""
    return f"{order[0]},{order[1]},{order[2]}"


def display_orders(orders):
    """Print all current orders."""
    print("Current Orders:")
    print()
    if not orders:
        print("No orders yet.")
    for order in orders:
        print(f"{order[0]}, {order[1]}, {order[2]}")
    print()


def get_next_id(orders):
    """Next order ID = highest existing ID + 1, or 1001 if there are no orders."""
    if not orders:
        return STARTING_ID
    return max(order[0] for order in orders) + 1


def get_product_name():
    """Ask for a product name until a valid one is entered.
    Returns 'quit' if the user wants to exit."""
    while True:
        name = input("Enter Product Name: ").strip()
        if name.lower() == "quit":
            return "quit"
        if name == "":
            print("Product name cannot be empty.")
        elif "," in name:
            print("Product name cannot contain commas.")
        else:
            return name


def get_quantity():
    """Ask for a quantity until a positive whole number is entered.
    Returns 'quit' if the user wants to exit."""
    while True:
        qty = input("Enter Quantity: ").strip()
        if qty.lower() == "quit":
            return "quit"
        if qty.isdigit() and int(qty) > 0:
            return int(qty)
        print("Invalid quantity. Please enter a positive whole number.")


def main():
    orders = load_orders()
    display_orders(orders)
    print("(Type 'quit' at any prompt to exit)")
    print()

    while True:  # keeps asking for orders until the user types quit
        product = get_product_name()
        if product == "quit":
            break

        quantity = get_quantity()
        if quantity == "quit":
            break

        new_order = [get_next_id(orders), product, quantity]
        orders.append(new_order)

        print()
        print("New Order Added:")
        print(format_order(new_order))

        save_orders(orders)  # save after every order so nothing is lost
        print()
        print(f"Order successfully saved to {ORDERS_FILE}")
        print()

    print()
    print(f"Exiting. Total orders saved: {len(orders)}")


if __name__ == "__main__":
    main()