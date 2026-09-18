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
    inventory = 0
    failures = 0

    print("=" * 40)
    print("Welcome to Smart Inventory Auditor")
    print("=" * 40)

    while True:
        result = get_valid_input()

        if result == "quit":
            break
        elif result is None:
            print("Invalid input. Please enter a number or 'quit'.")
            failures += 1
            continue

        inventory = process_delivery(inventory, result)
        print(f"Current inventory: {inventory}")

        tax = calculate_tax(result)
        print(f"Tax on this delivery: {tax}")

        if inventory > 500:
            print("ALERT: Inventory exceeded 500 units!")
            # no break — this is a warning, not a stop condition

    generate_report(inventory, failures)
    print(f"Exiting Smart Inventory Auditor. Final inventory: {inventory}")


if __name__ == "__main__":
    main()