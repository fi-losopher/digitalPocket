import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# Constants
FILE_NAME = "expenses.csv"

# Helper functions
def get_all_expenses():
    """Retrieve all expenses from the CSV file."""
    expenses = []
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            expenses = list(reader)
    except FileNotFoundError:
        pass
    return expenses

def save_expenses(expenses):
    """Save all expenses to the CSV file."""
    try:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(expenses)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def is_valid_date(date_str):
    """Check if the date is valid."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def add_expense():
    """Add a new expense to the table."""
    date = entry_date.get()
    category = entry_category.get()
    description = entry_description.get()
    amount = entry_amount.get()

    if not date or not category or not description or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return

    if not is_valid_date(date):
        messagebox.showerror("Error", "Invalid date format. Please use dd-mm-yyyy!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    # Append the new expense to the CSV
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Expense added successfully!")

def edit_expense():
    """Edit the selected expense."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to edit!")
        return

    index = tree.index(selected_item[0])  # Get the index of the selected item
    expenses = get_all_expenses()

    date = entry_date.get()
    category = entry_category.get()
    description = entry_description.get()
    amount = entry_amount.get()

    if not date or not category or not description or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return

    if not is_valid_date(date):
        messagebox.showerror("Error", "Invalid date format. Please use dd-mm-yyyy!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    # Update the selected expense in the list
    expenses[index] = [date, category, description, amount]
    save_expenses(expenses)

    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Expense edited successfully!")

def delete_expense():
    """Delete the selected expense."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete!")
        return

    index = tree.index(selected_item[0])
    expenses = get_all_expenses()
    del expenses[index]
    save_expenses(expenses)

    refresh_table()
    messagebox.showinfo("Success", "Expense deleted successfully!")

def refresh_table():
    """Refresh the table content."""
    for item in tree.get_children():
        tree.delete(item)
    for expense in get_all_expenses():
        tree.insert("", "end", values=expense)

def clear_fields():
    """Clear all input fields."""
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

def show_summary():
    """Show a summary of total expenses."""
    expenses = get_all_expenses()
    total = sum(float(expense[3]) for expense in expenses)
    categories = {}
    for expense in expenses:
        categories[expense[1]] = categories.get(expense[1], 0) + float(expense[3])
    summary = f"Total Expenses: {total:.2f}\n\nCategory-wise:\n"
    for category, amount in categories.items():
        summary += f"{category}: {amount:.2f}\n"
    messagebox.showinfo("Expense Summary", summary)

def toggle_theme():
    """Toggle between dark and light themes."""
    if root["bg"] == "#2c3e50":
        root.config(bg="#ffffff")
        style.configure("Treeview", background="#ffffff", foreground="#000000")
        style.configure("TButton", background="#d9d9d9", foreground="#000000")
    else:
        root.config(bg="#2c3e50")
        style.configure("Treeview", background="#2c3e50", foreground="#ecf0f1")
        style.configure("TButton", background="#34495e", foreground="#ecf0f1")

def export_data():
    """Export the expenses to a CSV file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(get_all_expenses())
            messagebox.showinfo("Success", "Expenses exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

def import_data():
    """Import expenses from a CSV file."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            with open(file_path, mode="r") as file:
                reader = csv.reader(file)
                expenses = list(reader)
            save_expenses(expenses)
            refresh_table()
            messagebox.showinfo("Success", "Expenses imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {e}")

def populate_fields(event):
    """Populate input fields when a row is double-clicked."""
    selected_item = tree.selection()
    if not selected_item:
        return
    values = tree.item(selected_item[0])['values']
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_date.insert(0, values[0])
    entry_category.insert(0, values[1])
    entry_description.insert(0, values[2])
    entry_amount.insert(0, values[3])

def search_expenses():
    """Search for expenses based on a query."""
    query = entry_search.get().lower()
    for item in tree.get_children():
        tree.delete(item)
    expenses = get_all_expenses()
    for expense in expenses:
        if query in expense[0].lower() or query in expense[1].lower() or query in expense[2].lower():
            tree.insert("", "end", values=expense)


def date():
    """Add the Date"""
    if root["bg"] == "#2c3e50":
        root.config(bg="#ffffff")
        style.configure("Treeview", background="#ffffff", foreground="#000000")
        style.configure("TButton", background="#d9d9d9", foreground="#000000")

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x600")
root.config(bg="#2c3e50")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25, background="#ecf0f1", foreground="#34495e", fieldbackground="#ecf0f1")
style.configure("TButton", font=("Arial", 10), background="#34495e", foreground="#ecf0f1")

# Input fields
frame_top = tk.Frame(root, bg="#2c3e50")
frame_top.pack(fill="x", padx=20, pady=10)

ttk.Label(frame_top, text="Date:").grid(row=0, column=0, padx=5, pady=5)
entry_date = ttk.Entry(frame_top)
entry_date.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_top, text="Category:").grid(row=0, column=2, padx=5, pady=5)
entry_category = ttk.Entry(frame_top)
entry_category.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(frame_top, text="Description:").grid(row=1, column=0, padx=5, pady=5)
entry_description = ttk.Entry(frame_top)
entry_description.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

ttk.Label(frame_top, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
entry_amount = ttk.Entry(frame_top)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root, bg="#2c3e50")
frame_buttons.pack(fill="x", padx=20, pady=10)

ttk.Button(frame_buttons, text="Add Expense", command=add_expense).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Edit Expense", command=edit_expense).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Delete Expense", command=delete_expense).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Summary", command=show_summary).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Export", command=export_data).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Import", command=import_data).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Toggle Theme", command=toggle_theme).pack(side="left", padx=5)

# Expense table setup
frame_table = tk.Frame(root, bg="#2c3e50")
frame_table.pack(fill="both", expand=True, padx=20, pady=10)

tree = ttk.Treeview(frame_table, columns=("Date", "Category", "Description", "Amount"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.heading("Amount", text="Amount")
tree.pack(fill="both", expand=True)

# Add the event binding for populating fields
tree.bind("<Double-1>", populate_fields)

# Search bar
search_frame = tk.Frame(root, bg="#2c3e50")
search_frame.pack(pady=10)

ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_search = ttk.Entry(search_frame, width=30)
entry_search.grid(row=0, column=1, padx=5, pady=5)
search_button = ttk.Button(search_frame, text="Search", command=search_expenses)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Populate table with data when the app starts
refresh_table()

# Start the Tkinter event loop
root.mainloop()
