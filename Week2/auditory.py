inventory = 0
failure = 0
####
while True:
    user_input = input("Enter stock quantity (or 'quit'): ")

    if user_input.lower() == "quit":
        break
    elif not user_input.isdigit():
        print("Error: Invalid input.")
        failure += 1
        continue

    stock = int(user_input)
    if stock < 0:
        print("Error: Negative numbers not allowed.")
        failure += 1
        continue

    inventory += stock
    if inventory > 500:
        print("ALERT: Inventory exceeded 500 units!")
        break

print(f"Total Units Processed: {inventory}")
print(f"Number of Failed Entries: {failure}")

