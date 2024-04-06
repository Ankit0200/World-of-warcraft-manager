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

from tqdm import tk


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


class Class_manager:
    def __init__(self,root):
        self.root = root
        self.root.title("World of Warcraft Management")
        self.root.geometry("1100x580+260+130")
        # self.root.configure(background="#000025")

        self.class_name=StringVar()


        self.Main_frame = Frame(self.root, bg="lightyellow", height=450, width=700, bd=5, relief=RIDGE)
        self.Main_frame.place(x=220, y=50)

        Class_name_lbl=Label(self.Main_frame, text="Class Name:",bg="lightyellow", fg="black",font=('Times New Roman', 20,'bold'),width=10)
        Class_name_lbl.place(x=10,y=120)

        Class_name_entry = Entry(self.Main_frame, font=('Times New Roman', 17,'bold'),width=15,textvariable=self.class_name)
        Class_name_entry.place(x=170,y=125)

        Add_Button = Button(self.Main_frame, text="Add", font=("Times New Roman", 15), bg='green', fg='white',command=self.add)
        Add_Button.place(x=15, y=200, width=100)

        Delete_Button = Button(self.Main_frame, text="Delete", font=("Times New Roman", 15,'bold'), bg='red', fg='black',command=self.delete)
        Delete_Button.place(x=140, y=200, width=100)

        Clear_Button = Button(self.Main_frame, text="Clear", font=("Times New Roman", 15,'bold'), bg='gray', fg='black',command=self.clear)
        Clear_Button.place(x=270, y=200, width=100)


        ##### CLASS NAME LISTBOX =====================
        class_viewing_frame = Frame(self.Main_frame, width=350, height=170, bg="green")

        class_viewing_frame.place(x=420, y=120)
        self.Class_list = Listbox(class_viewing_frame, font=("Times New Roman", 15, "bold"), bg="lightblue",
                                  relief=RIDGE, bd=2, height=7)

        scrolly_w = Scrollbar(class_viewing_frame, orient=VERTICAL, command=self.Class_list.yview)
        scrollx_w = Scrollbar(class_viewing_frame, orient=HORIZONTAL, command=self.Class_list.xview, width=4)

        self.Class_list.config(yscrollcommand=scrolly_w.set, xscrollcommand=scrollx_w.set)

        scrolly_w.pack(side=RIGHT, fill=Y)
        scrollx_w.pack(side=BOTTOM, fill=X)

        self.Class_list.pack(fill=BOTH, expand=True)

        view_info_lbl = Label(self.root, text="View Classes", font=("Times New Roman", 20, "bold"), bg="green",
                              fg="white",width=13,
                               bd=2, relief=RIDGE)
        view_info_lbl.place(x=644, y=130)

        self.Class_list.bind('<ButtonRelease-1>', self.get_classes)

        self.show_classes()


    def add(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        if self.class_name.get()!='':
            cursor.execute('Select * from classes where Class=?',(self.class_name.get(),))
            classes=cursor.fetchall()
            if len(classes)>0:
                messagebox.showerror("Error", "Class already exists")
            else:
                cursor.execute('INSERT INTO Classes (Class) VALUES (?)',(self.class_name.get(),))
                conn.commit()
                messagebox.showinfo("Success", "Class added successfully")
                self.show_classes()
                self.clear()


    def show_classes(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT Class from Classes')
        classes=cursor.fetchall()
        if len(classes)>0:
            self.Class_list.delete(0, END)
            for char in classes:
                self.Class_list.insert(END,char)

    def delete(self):
        index_ = self.Class_list.curselection()
        name = self.Class_list.get(index_)
        # name=name[0]
        print(name)
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('Select * from Classes where Class=?',(name))
        row=cursor.fetchall()
        print(row)
        if len(row)>0:
           is_sure=messagebox.askyesno('Confirmation', f'Do you sure want to delete this class?\n \t\t{name[0]}', parent=self.root)

           if is_sure:
               cursor.execute('DELETE FROM Classes WHERE Class=?',(name))
               conn.commit()
               messagebox.showinfo("Deleted", "Class deleted successfully ")
               self.show_classes()


    def clear(self):
        self.class_name.set('')

    def get_classes(self,ev):
        index_ = self.Class_list.curselection()
        name = self.Class_list.get(index_)
        self.class_name.set(name)





if __name__ == "__main__":
    root = Tk()
    Class_manager(root)
    root.mainloop()