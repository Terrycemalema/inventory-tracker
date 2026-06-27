inventory = []

def add_item():
    name = input("Item name: ")
    quantity = int(input("Item quantity: "))

    item = {
        "name": name,
        "quantity": quantity
    }

    inventory.append(item)
    print("Item added successfully!")

def view_item():
    if len(inventory) == 0:
        print("No items available.")
    else:
        print("\nINVENTORY LIST")
        for item in inventory:
            print(item["name"], "-", item["quantity"])

while True:
    print("\nINVENTORY MENU")
    print("1. Add item")
    print("2. View item")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_item()

    elif choice == "2":
        view_item()

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")