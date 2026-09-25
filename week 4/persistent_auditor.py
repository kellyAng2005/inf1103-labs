import os

INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """Read the saved total and transaction history from the inventory file.

    If the file does not exist (or is unreadable/corrupt), start fresh
    with an empty inventory and no history, without raising an error.
    """
    if not os.path.exists(INVENTORY_FILE):
        return 0, []

    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.read().splitlines()

        if not lines:
            return 0, []

        total = int(lines[0])
        history = [int(line) for line in lines[1:] if line.strip() != ""]
        return total, history
    except (ValueError, IndexError):
        return 0, []


def save_inventory(total, history):
    """Write the final total and transaction history list to the inventory file."""
    with open(INVENTORY_FILE, "w") as f:
        f.write(f"{total}\n")
        for amount in history:
            f.write(f"{amount}\n")


def get_valid_input():
    """Prompt for a stock quantity. Returns an int, or the string 'quit'."""
    user_input = input("Enter stock quantity (or 'quit' to exit): ")

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        return None  # invalid entry

    return int(user_input)


def process_delivery(current_total, new_value):
    """Add the new delivery to the running total and return the new total."""
    return current_total + new_value


def calculate_tax(amount):
    """Return 10% tax on a single delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Print the final summary."""
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    inventory, history = load_inventory()
    failures = 0

    print("=" * 40)
    print("Welcome to Persistent Inventory Auditor")
    print("=" * 40)
    print(f"Loaded inventory: {inventory}")
    print(f"Loaded transaction history: {history}")

    while True:
        result = get_valid_input()

        if result == "quit":
            break
        elif result is None:
            print("Invalid input. Please enter a number or 'quit'.")
            failures += 1
            continue

        inventory = process_delivery(inventory, result)
        history.append(result)
        print(f"Current inventory: {inventory}")

        tax = calculate_tax(result)
        print(f"Tax on this delivery: {tax}")

        if inventory > 500:
            print("ALERT: Inventory exceeded 500 units!")
            # no break — this is a warning, not a stop condition

    save_inventory(inventory, history)
    generate_report(inventory, failures)
    print(f"Exiting Persistent Inventory Auditor. Final inventory: {inventory}")
    print(f"Transaction history: {history}")
    print(f"Inventory successfully saved to {INVENTORY_FILE}")


if __name__ == "__main__":
    main()
