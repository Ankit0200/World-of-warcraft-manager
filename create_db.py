import sqlite3
import os
import sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def connect_to_database():
    # Construct the path to the database file
    database_path = resource_path('world_of_warcraft.db')

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        print("Database connected successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_databases(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Players (
                        Player_id INTEGER PRIMARY KEY,
                        Username TEXT,
                        Password TEXT,
                        in_game_tag TEXT,
                        Class Text,
                        Role_in_raid TEXT,
                        Role_in_Guild TEXT
                     )''')
    conn.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Admin(Username Text, Password Text)')
    conn.commit()

    cursor.execute('CREATE TABLE IF NOT EXISTS wishlist(Ig_tag TEXT, Wishlist Text)')
    conn.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS Boss(Boss_name TEXT, Rewards Text)')
    conn.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS loots(Loot_name TEXT,Boss_name TEXT,Class Text)')
    conn.commit()
    cursor.execute('Create TABLE IF NOT EXISTS Classes(id integer Primary KEY ,Class Text)')
    conn.commit()
    cursor.close()


# Connect to the database
conn = connect_to_database()

# Create tables if the connection is successful
if conn is not None:
    create_databases(conn)
else:
    print("Failed to connect to the database.")
