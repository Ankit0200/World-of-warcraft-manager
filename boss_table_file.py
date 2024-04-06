import os
import tkinter
import tkinter.ttk

from tkinter import *
from tkinter import filedialog,simpledialog,messagebox
from PIL import ImageTk, Image

import ast

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
      # Debugging statement

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)

        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database Error: {e}")


class Bosstable:
    def __init__(self,root):
        self.root = root
        self.root.title("World of Warcraft Management")
        self.root.geometry("1100x580+260+130")
        # self.root.configure(background="#000025")

        self.Detail_frame=Frame(self.root, bg="lightyellow", height=500, width=400, bd=5, relief=RIDGE)
        self.Detail_frame.place(x=550, y=20)

        #### VARIABLES ++++++++++++++++++++++
        self.Boss_name=StringVar()
        self.rewards=Listbox()
        self.my_new_boss=StringVar()

        # ------------------- Boss TEE TREE VIEW NOW -----------------------+
        Boss_table_frame = Frame(self.root, bg="lightyellow", bd=2, relief=RIDGE)
        Boss_table_frame.place(x=15, y=28, width=405, height=410)

        scrolly = Scrollbar(Boss_table_frame, orient=VERTICAL)
        scrollx = Scrollbar(Boss_table_frame, orient=HORIZONTAL)
        #

        self.boss_table = tkinter.ttk.Treeview(Boss_table_frame, columns=(
            "Boss", "Rewards"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrolly.config(command=self.boss_table.yview)
        scrollx.config(command=self.boss_table.xview)

        self.boss_table.heading("Boss", text='Boss')
        self.boss_table.heading("Rewards", text='Rewards')

        self.boss_table.bind('<<TreeviewSelect>>', self.get_data)
        self.boss_table['show'] = 'headings'
        self.boss_table.column('Boss', width=40)
        self.boss_table.column('Rewards', width=150)
        self.boss_table.pack(fill=BOTH, expand=1)
        self.fetch_boss()

        ##### Modifying boss ++++++++++++++++++++++++++++++++++++++++++

        New_boss=Label(self.root, text="New Boss:", font=("Times new roman", 15, "bold"))
        New_boss.place(x=10,y=500)

        New_boss_entry=Entry(self.root, font=("Times new roman",15, "bold"), width=15,textvariable=self.my_new_boss)
        New_boss_entry.place(x=110,y=500)

        Add_button=Button(self.root, text="Add",font=("Times new roman", 10, "bold"), width=15, command=self.new_boss,bg='pink',activebackground='lightgreen',activeforeground='red')
        Add_button.place(x=300,y=500)









        ### LABELS AND ENTRIES ===========================

        Boss=Label(self.Detail_frame, text="Boss Name:", font=("Times New Roman", 15,"bold"), bg="lightyellow")
        Boss.place(x=24,y=44)

        Rewards=Label(self.Detail_frame, text="Rewards:", font=("Times New Roman", 15,"bold"), bg="lightyellow")
        Rewards.place(x=24,y=105)

        Boss_entry=Entry(self.Detail_frame, font=("Times New Roman", 15,"bold"),bg="lightblue",textvariable=self.Boss_name,width=23,bd=2,relief=RIDGE)
        Boss_entry.place(x=140,y=44)


        Wishlist_listing_frame=Frame(self.Detail_frame, width=240, height=280, bg="green")
        Wishlist_listing_frame.place(x=140,y=110)

        self.rewards_list=Listbox(Wishlist_listing_frame, font=("Times New Roman",15,"bold"),bg="lightblue",width=20,relief=RIDGE,bd=2)

        scrolly_w=Scrollbar(Wishlist_listing_frame, orient=VERTICAL,command=self.rewards_list.yview)
        scrolly_w.pack(side=RIGHT, fill=Y)

        scrollx_w=Scrollbar(Wishlist_listing_frame,orient=HORIZONTAL,command=self.rewards_list.xview)
        scrollx_w.pack(side=BOTTOM,fill=X)
        self.rewards_list.pack(side=LEFT, fill=Y)




    def new_boss(self):
        if self.my_new_boss.get()=="":
            messagebox.showerror("Error", "Please enter a new boss name to add",parent=self.root)
        else:
            try:
                conn=connect_to_database()
                cursor=conn.cursor()
                cursor.execute('Select * from Boss where Boss_name=?',(self.my_new_boss.get(),))
                rows=cursor.fetchall()
                if len(rows)>0:
                    messagebox.showerror("Error", "The boss already exists",parent=self.root)
                else:
                    cursor.execute('INSERT INTO Boss (Boss_name) VALUES (?)', (self.my_new_boss.get(),))
                    conn.commit()
                    messagebox.showinfo("Success", "Boss added successfully", parent=self.root)

                    self.fetch_boss()
                    self.my_new_boss.set('')

            except Exception as e:
                messagebox.showerror("Error",f"Error hora due to \n{e}",parent=self.root)


    def get_data(self,ev):
        selected_item = self.boss_table.focus()  # Get the selected item in the Treeview
        if selected_item:  # Ensure an item is selected
            item_values = self.boss_table.item(selected_item, 'values')  # Get the values of the selected item
            if item_values:  # Ensure values exist
                self.Boss_name.set(item_values[0])
                # my_list=ast.literal_eval(item_values[1])
                self.rewards_list.delete(0,END)
                print(item_values[1].split(','))
                for char in item_values[1].split(','):
                    self.rewards_list.insert(END,char)



    def fetch_boss(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('Select * from Boss')
        rows=cursor.fetchall()


        if len(rows)>0:
            self.boss_table.delete(*self.boss_table.get_children())
            for char in rows:
                self.boss_table.insert('',END, values=char)



























if __name__ == "__main__":
    root=Tk()
    Bosstable(root)
    root.mainloop()
