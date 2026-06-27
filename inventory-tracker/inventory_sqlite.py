import sqlite3


connection = sqlite3.connect("inventory.db")


cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

connection.commit()


def add_item():
    name = input("Item name: ")
    quantity = int(input("Item quantity: "))

    cursor.execute("""
    INSERT INTO inventory (name, quantity)
    VALUES (?, ?)
    """, (name, quantity))

    connection.commit()
    print("Item added successfully!")


def view_items():
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    if len(items) == 0:
        print("No items available.")
    else:
        print("\nINVENTORY LIST")
        for item in items:
            print("ID:", item[0], "| Name:", item[1], "| Quantity:", item[2])


def search_item():
    name = input("Enter item name to search: ")

    cursor.execute("""
    SELECT * FROM inventory
    WHERE name LIKE ?
    """, ("%" + name + "%",))

    items = cursor.fetchall()

    if len(items) == 0:
        print("Item not found.")
    else:
        print("\nSEARCH RESULTS")
        for item in items:
            print("ID:", item[0], "| Name:", item[1], "| Quantity:", item[2])


def update_item():
    item_id = int(input("Enter item ID to update: "))
    new_quantity = int(input("Enter new quantity: "))

    cursor.execute("""
    UPDATE inventory
    SET quantity = ?
    WHERE id = ?
    """, (new_quantity, item_id))

    connection.commit()

    if cursor.rowcount == 0:
        print("Item not found.")
    else:
        print("Item updated successfully!")


def delete_item():
    item_id = int(input("Enter item ID to delete: "))

    cursor.execute("""
    DELETE FROM inventory
    WHERE id = ?
    """, (item_id,))

    connection.commit()

    if cursor.rowcount == 0:
        print("Item not found.")
    else:
        print("Item deleted successfully!")


while True:
    print("\nINVENTORY MENU")
    print("1. Add item")
    print("2. View items")
    print("3. Search item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_item()

    elif choice == "2":
        view_items()

    elif choice == "3":
        search_item()

    elif choice == "4":
        update_item()

    elif choice == "5":
        delete_item()

    elif choice == "6":
        print("Goodbye!")
        connection.close()
        break

    else:
        print("Invalid choice. Please try again.")