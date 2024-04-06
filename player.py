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
    database_path = resource_path('database/world_of_warcraft.db')
    print("Database path:", database_path)  # Debugging statement

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        print("Database connected successfully!")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")

class playerCard:
    def __init__(self,root):
        self.root = root
        self.root.title("World of Warcraft Management")
        self.root.geometry("630x480+510+200")


        #---- USERNAME --------+
        if len(sys.argv) > 1:
            # The username is the first argument after the script name
            print(sys.argv)
            self.username = sys.argv[1]
            self.password =sys.argv[2]
            self.Ig_tag=sys.argv[3]
            self.class_of=sys.argv[4]
            self.role_ing_raid=sys.argv[5]
            self.role_ing_guild=sys.argv[6]
        else:
            self.username = "not set"
            self.password = "not set"
            self.Ig_tag = "not set"
            self.class_of = "not set"
            self.role_ing_raid = "not set"
            self.role_ing_guild = "not set"

        ##----- Title Label------------+

        self.title = Label(self.root, text=f"Player card",
                           font=("Times New Roman", 25, "bold"), bg='green', fg='yellow', anchor='center',
                           justify='center')
        self.title.place(x=0, y=0, height=40, relwidth=1)

        ##===++= PLAYER INFO ===========================
        # Create the frame for player card
        Player_card_frame = Frame(self.root, bg='lightyellow', relief=RIDGE, bd=3)
        Player_card_frame.place(x=50, y=65, height=350, width=510)

        # Create the text widget
        self.player = Text(Player_card_frame, font=("Times New Roman", 15,'bold'), bg='lightyellow', bd=2, relief=RIDGE)


        # Create the vertical scrollbar
        scrolly = Scrollbar(Player_card_frame, orient=VERTICAL, command=self.player.yview)
        scrolly.pack(side=RIGHT, fill=Y)

        # Create the horizontal scrollbar
        scrollx = Scrollbar(Player_card_frame, orient=HORIZONTAL, command=self.player.xview)
        scrollx.pack(side=BOTTOM, fill=X)

        # Configure the text widget to use the scrollbars
        self.player.config(yscrollcommand=scrolly.set)
        self.player.config(xscrollcommand=scrollx.set)
        self.player.pack(side=LEFT, fill=BOTH, expand=1)

        self.generate_card()

        wish_list_button=Button(self.root, text="View wishlist", command=self.view_wish, font=("Times New Roman",15,'bold'), bg='lightgreen', relief=RIDGE)
        wish_list_button.place(x=400, y=420)
    def view_wish(self):
        self.root.destroy()
        os.system(f'python wishlist.py {self.Ig_tag}')

    def generate_card(self):
        self.player.delete(1.0, END)

        template=f"""   
      
        
        UserName:{self.username}                 Password:{self.password}
    
    
    
        IG_tag:{self.Ig_tag}                   Role in raid: {self.role_ing_raid}
        
        
        Role in guild: {self.role_ing_guild}
                                 
        
        """
        self.player.insert(END, template)





if __name__ == "__main__":
    root = tkinter.Tk()
    playerCard(root)
    root.mainloop()


