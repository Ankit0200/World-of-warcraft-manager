import os
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, Label, Button
from PIL import ImageTk, Image
import os,sys
from create_db import create_databases

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("400x450+510+150")
        self.root.configure(background="white")

        self.username = StringVar()
        self.password = StringVar()
        self.login_type = StringVar()

        login_type_lbl = Label(self.root, text="Login Type:", font=("Times New Roman", 14), bg='white')
        login_type_lbl.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.login_type_combo = ttk.Combobox(self.root, width=20, values=('Admin', 'Player'),
                                             font=("Times New Roman", 12, 'bold'), state='readonly',
                                             textvariable=self.login_type)
        self.login_type_combo.place(relx=0.5, rely=0.15, anchor=CENTER)
        self.login_type_combo.current(0)

        loging_frame = Frame(self.root, bg="white", relief=RIDGE, bd=5)
        loging_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        login_label = Label(loging_frame, text="Login System", font=("Times New Roman", 25, "bold"), bg="white",)
        login_label.grid(row=0, columnspan=2, pady=20)

        user_name_lbl = Label(loging_frame, text="Username:", font=("Times New Roman", 14), bg='white')
        user_name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        user_name_entry = Entry(loging_frame, font=("Times New", 14), bg='lightyellow', fg='black',
                                textvariable=self.username, show="*")
        user_name_entry.grid(row=1, column=1, padx=10, pady=10)

        password_lbl = Label(loging_frame, text="Password:", font=("Times New Roman", 14), bg='white')
        password_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        password_entry = Entry(loging_frame, font=("Times New", 14), bg='lightyellow', fg='black',
                               textvariable=self.password, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        login_button = Button(loging_frame, text="Login/Register", font=("Times New", 14, "bold"),
                              bg='blue', fg='white', command=self.login_now)
        login_button.grid(row=3, columnspan=2, pady=20)

    def login_now(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please enter all fields", parent=self.root)
        else:
            database_path = resource_path('world_of_warcraft.db')
            conn = sqlite3.connect(database_path)
            cur = conn.cursor()

            if self.login_type.get()=='Admin':
                cur.execute("SELECT * FROM Admin")
                rows = cur.fetchone()
                if rows is None:
                    messagebox.showerror("Error", "Please setup admin", parent=self.root)
                else:
                    if self.username.get()==rows[0] and self.password.get()==rows[1]:
                        self.root.destroy()
                        os.system("python " + resource_path("admin.py"))
            elif self.login_type.get()=='Player':
                cur.execute('SELECT * FROM Players')
                rows = cur.fetchall()
                for row in rows:
                    if self.username.get()==row[0] and self.password.get()==row[1]:
                        self.root.destroy()
                        print(row)
                        name=row[0]
                        password=row[1]
                        in_game_tag=row[2]
                        class_of=row[3]
                        R_i_r=row[4]
                        r_i_g=row[5]

                        os.system(f"python " + resource_path("player.py") + f" {name} {password} {in_game_tag} {class_of} {R_i_r} {r_i_g}")

if __name__ == "__main__":
    database_path = resource_path('world_of_warcraft.db')
    conn = sqlite3.connect(database_path)
    root = Tk()
    LoginClass(root)
    root.mainloop()
