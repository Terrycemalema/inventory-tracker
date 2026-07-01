import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------- DATABASE SETUP ----------------

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
    name = name_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if name == "" or quantity == "":
        messagebox.showwarning("Input Error", "Please enter both item name and quantity.")
        return

    try:
        quantity = int(quantity)
        if quantity < 0:
            messagebox.showwarning("Input Error", "Quantity cannot be negative.")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Quantity must be a number.")
        return

    cursor.execute("""
    INSERT INTO inventory (name, quantity)
    VALUES (?, ?)
    """, (name, quantity))

    connection.commit()

    messagebox.showinfo("Success", "Item added successfully!")
    clear_entries()
    view_items()


def view_items():
    for row in inventory_table.get_children():
        inventory_table.delete(row)

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    for item in items:
        inventory_table.insert("", tk.END, values=item)


def search_item():
    search_name = search_entry.get().strip()

    for row in inventory_table.get_children():
        inventory_table.delete(row)

    cursor.execute("""
    SELECT * FROM inventory
    WHERE name LIKE ?
    """, ("%" + search_name + "%",))

    items = cursor.fetchall()

    for item in items:
        inventory_table.insert("", tk.END, values=item)


def select_item(event):
    selected = inventory_table.focus()

    if selected:
        values = inventory_table.item(selected, "values")

        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)

        id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        quantity_entry.insert(0, values[2])


def update_item():
    item_id = id_entry.get().strip()
    name = name_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if item_id == "":
        messagebox.showwarning("Selection Error", "Please select an item to update.")
        return

    if name == "" or quantity == "":
        messagebox.showwarning("Input Error", "Please enter item name and quantity.")
        return

    try:
        quantity = int(quantity)
        if quantity < 0:
            messagebox.showwarning("Input Error", "Quantity cannot be negative.")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Quantity must be a number.")
        return

    cursor.execute("""
    UPDATE inventory
    SET name = ?, quantity = ?
    WHERE id = ?
    """, (name, quantity, item_id))

    connection.commit()

    messagebox.showinfo("Success", "Item updated successfully!")
    clear_entries()
    view_items()


def delete_item():
    item_id = id_entry.get().strip()

    if item_id == "":
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")

    if confirm:
        cursor.execute("""
        DELETE FROM inventory
        WHERE id = ?
        """, (item_id,))

        connection.commit()

        messagebox.showinfo("Success", "Item deleted successfully!")
        clear_entries()
        view_items()


def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)


def check_low_stock():
    cursor.execute("""
    SELECT * FROM inventory
    WHERE quantity < 5
    """)

    low_stock_items = cursor.fetchall()

    if len(low_stock_items) == 0:
        messagebox.showinfo("Low Stock", "No low stock items.")
    else:
        message = "Low stock items:\n\n"

        for item in low_stock_items:
            message += f"{item[1]} - Quantity: {item[2]}\n"

        messagebox.showwarning("Low Stock Alert", message)


def close_app():
    connection.close()
    root.destroy()



root = tk.Tk()
root.title("Inventory Tracker")
root.geometry("750x500")



input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="ID").grid(row=0, column=0, padx=5, pady=5)
id_entry = tk.Entry(input_frame, width=10)
id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Item Name").grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame, width=30)
name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(input_frame, width=30)
quantity_entry.grid(row=2, column=1, padx=5, pady=5)


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Item", width=15, command=add_item).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Item", width=15, command=update_item).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Item", width=15, command=delete_item).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear", width=15, command=clear_entries).grid(row=0, column=3, padx=5)



search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search Item").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

tk.Button(search_frame, text="Search", width=15, command=search_item).grid(row=0, column=2, padx=5)
tk.Button(search_frame, text="View All", width=15, command=view_items).grid(row=0, column=3, padx=5)
tk.Button(search_frame, text="Low Stock", width=15, command=check_low_stock).grid(row=0, column=4, padx=5)


# ---------------- TABLE ----------------

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("ID", "Name", "Quantity")

inventory_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

inventory_table.heading("ID", text="ID")
inventory_table.heading("Name", text="Item Name")
inventory_table.heading("Quantity", text="Quantity")

inventory_table.column("ID", width=100)
inventory_table.column("Name", width=300)
inventory_table.column("Quantity", width=150)

inventory_table.pack()

inventory_table.bind("<ButtonRelease-1>", select_item)



tk.Button(root, text="Exit", width=20, command=close_app).pack(pady=10)


view_items()

root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()