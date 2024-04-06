import os
import tkinter
import tkinter.ttk
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox, ttk
import sqlite3


# Function to connect to the SQLite database
def connect_to_database():
    # Construct the path to the database file
    database_path = "world_of_warcraft.db"  # Change this to your database file path
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database Error: {e}")


# Function to create a table if it doesn't exist
def create_table_if_not_exists():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        # Create a table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS your_table_name (
                id INTEGER PRIMARY KEY,
                column_name TEXT
            )
        """)
        # Commit the changes to the database
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database Error: {e}")
    finally:
        # Close the database connection
        conn.close()


# Function to add elements from a list to the database
def add_elements_to_database(data_list):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Iterate over the list and insert each element into the database
        for item in data_list:
            cursor.execute("INSERT INTO your_table_name (column_name) VALUES (?)", (item,))

        # Commit the changes to the database
        conn.commit()
        messagebox.showinfo("Success", "Elements added to the database successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database Error: {e}")
    finally:
        # Close the database connection
        conn.close()


class AddToListDatabase:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Elements to Database")
        self.root.geometry("400x200")

        # Entry widget to enter elements
        self.entry = Entry(root, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Button to add elements to the list
        self.add_button = Button(root, text="Add Element", command=self.add_element)
        self.add_button.pack()

    def add_element(self):
        # Get the value from the entry widget
        element = self.entry.get()
        # Add the element to the list
        data_list.append(element)
        # Clear the entry widget
        self.entry.delete(0, 'end')

        # Call function to add elements to the database
        add_elements_to_database([element])


if __name__ == "__main__":
    # Create an empty list to store elements
    data_list = []

    # Create the main Tkinter window
    root = Tk()
    # Create a table if it doesn't exist
    create_table_if_not_exists()
    # Create an instance of the AddToListDatabase class
    app = AddToListDatabase(root)
    # Run the Tkinter event loop
    root.mainloop()
