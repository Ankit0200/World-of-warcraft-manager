import os
import tkinter
from tkinter import *
from PIL import ImageTk, Image

import sqlite3
import datetime

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
    print("Database path:", database_path)  # Debugging statement

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        print("Database connected successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")


class WCF:
    def __init__(self, root):
        self.root = root
        self.root.title("World of Warcraft Management")
        self.root.geometry("1366x768+0+0")
        self.current_window = None

        ##----- Title Label------------+

        self.title = Label(self.root, text="WORLD OF WARCRAFT MANAGER",
                           font=("Times New Roman", 25, "bold"), bg='green', fg='yellow', anchor='center',
                           justify='center')
        self.title.place(x=0, y=0, height=70, relwidth=1)

        ##=== LOGOUT BUTTON ==============================
        btn_logout = Button(self.root, command=self.logout_func, text="LOGOUT", font=('Times New Roman', 15, "bold"),
                            bg='yellow', fg='black', cursor='hand2')
        btn_logout.place(x=1150, y=10, height=50, width=150)
        ## LEFT FRAME ==========================
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        LeftMenu.place(x=10, y=105, width=250, height=650)

        self.Left_menu_logo = Image.open(resource_path("images/menu image1.png"))
        self.Left_menu_logo.thumbnail((320, 230))
        self.Left_menu_logo = ImageTk.PhotoImage(self.Left_menu_logo)
        lbl_menulogo = Label(LeftMenu, image=self.Left_menu_logo)
        lbl_menulogo.image = self.Left_menu_logo
        lbl_menulogo.pack(side=TOP, fill=X)

        # +++++++++  MENU =============================

        self.icon_btn = Image.open(resource_path("images/menu.png"))
        self.icon_btn.thumbnail((15, 15))
        self.icon_btn = ImageTk.PhotoImage(self.icon_btn)
        Menu = Label(LeftMenu, text="Menu", fg='white', font=("Times New Roman", 20, "bold"), bg='green', relief=RIDGE,
                     bd=2)
        btn_players = Button(LeftMenu, text="Players", fg='black',
                             font=("Times New Roman", 20, "bold"), cursor='hand2', image=self.icon_btn, compound=LEFT,
                             command=self.players_view,
                             bg='white', relief=RIDGE, bd=2)
        btn_Boss = Button(LeftMenu, text="Boss", fg='black',
                          font=("Times New Roman", 20, "bold"), image=self.icon_btn, cursor='hand2', compound=LEFT,
                          command=self.boss_table,
                          bg='white', relief=RIDGE, bd=2)
        btn_wishlist = Button(LeftMenu, text="Wishlist", fg='black',
                              font=("Times New Roman", 20, "bold"), image=self.icon_btn, cursor='hand2', compound=LEFT,
                              command=self.wishlist_func,
                              bg='white', relief=RIDGE, bd=2)
        btn_loot = Button(LeftMenu, text="Loot", fg='black', font=("Times New Roman", 20, "bold"),
                          image=self.icon_btn, compound=LEFT, bg='white', cursor='hand2', relief=RIDGE, bd=2,
                          command=self.loot_func)
        btn_class = Button(LeftMenu, text="Class", fg='black', font=("Times New Roman", 20, "bold"),
                           image=self.icon_btn, compound=LEFT, bg='white', cursor='hand2', relief=RIDGE, bd=2,
                           command=self.class_btn)

        btn_players.image = self.icon_btn
        btn_class.image = Button(LeftMenu, image=self.icon_btn)

        btn_Boss.image = self.icon_btn
        btn_loot.image = self.icon_btn
        btn_wishlist.image = self.icon_btn

        Menu.pack(side=TOP, fill=X)
        btn_class.pack(side=TOP, fill=X)
        btn_players.pack(side=TOP, fill=X)
        btn_Boss.pack(side=TOP, fill=X)
        btn_loot.pack(side=TOP, fill=X)
        btn_wishlist.pack(side=TOP, fill=X)

    def logout_func(self):
        self.root.destroy()
        os.system("python " + resource_path("login_file.py"))

    def players_view(self):
        self.destroy_current_window()
        os.system("python " + resource_path("admin_player.py"))

    def boss_table(self):
        self.destroy_current_window()
        os.system("python " + resource_path("boss_table_file.py"))

    def loot_func(self):
        self.destroy_current_window()
        os.system("python " + resource_path("loot.py"))

    def wishlist_func(self):
        self.destroy_current_window()
        os.system("python " + resource_path("wishlist.py") + " admin")

    def class_btn(self):
        self.destroy_current_window()
        os.system("python " + resource_path("classes_manager.py"))

    def destroy_current_window(self):
        # Destroy the current window if it exists and it's not a main panel
        if self.current_window and "panel" not in str(self.current_window).lower():
            self.current_window.destroy()
            self.current_window = None


if __name__ == "__main__":
    root = tkinter.Tk()
    WCF(root)
    root.mainloop()
