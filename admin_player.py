import tkinter.ttk
from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox,ttk,simpledialog
import os,sys
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


class ProductClass:
    def __init__(self,root):
        self.root =root
        self.root.title("World of Warcraft")
        self.root.geometry("1100x580+260+130")
        self.root.configure(bg="white")


  ##==------------------------VARIABLES----------------------------------------------------------------------------------------
        self.Username=StringVar()
        self.id_var=StringVar()
        self.username_for_search=StringVar()
        self.Password = StringVar()
        self.Role_in_guild=StringVar()
        self.Role_in_raid=StringVar()
        self.IG_tag=StringVar()
        self.class_name=StringVar()



#========================================================================================================================

        player_detail_frame=Frame(self.root,bg="white",height=500,width=600,bd=3,relief=RIDGE)
        player_detail_frame.place(x=30,y=30,width=500,height=540)



        self.root.focus_force()
        managing_label = Label(player_detail_frame, text="Manage Players",font=('Times new roman',18,'bold'), bg="#E0F2F1", fg="#001F3F")
        managing_label.pack(side=TOP, fill=X)


        #++++  labels #+++++


        Username=Label(player_detail_frame, font=('Times new roman',15),text="Username",bg='white',anchor='w')
        Username.place(x=20,y=170,width=200,height=25)

        IG_Role=Label(player_detail_frame, font=('Times new roman',15),text="Role in game",bg='white',anchor='w')
        IG_Role.place(x=20, y=220, width=200, height=25)

        Role_in_Guild=Label(player_detail_frame, font=('Times new roman',15),text="Role in Guild",bg='white',anchor='w')
        Role_in_Guild.place(x=20, y=270, width=200, height=25)

        IG_tag_lbl=Label(player_detail_frame, font=('Times new roman',15),text="Tag",bg='white',anchor='w')
        IG_tag_lbl.place(x=20,y=320 , width=200, height=25)

        Class_tag_lbl=Label(player_detail_frame, font=('Times new roman',15,),text="Class",bg='white',anchor='w')
        Class_tag_lbl.place(x=20,y=355, width=200, height=25)

        id_lbl=Label(player_detail_frame, font=('Times new roman',15),text="ID",bg='white',anchor='w',fg='black')
        id_lbl.place(x=20,y=100)


     #------------------------ENTRIES---------------------------------------------------------------------------


        Username_entry = Entry(player_detail_frame, textvariable=self.Username,
                                      font=('Times new roman', 15))
        Username_entry.place(x=150, y=170, width=200, height=25)


        IG_Role_entry=Entry(player_detail_frame,textvariable=self.Role_in_raid,font=('Times new Roman',15))
        IG_Role_entry.place(x=150,y=221,width=200,height=25)


        Role_ing_guild_entry = Entry(player_detail_frame, font=('Times new roman', 15),textvariable=self.Role_in_guild, bg='lightyellow')
        Role_ing_guild_entry.place(x=150, y=271, width=200, height=25)
        #
        IG_tag_entry = Entry(player_detail_frame, font=('Times new roman', 15), bg='lightyellow',textvariable=self.IG_tag)
        IG_tag_entry.place(x=150, y=321, width=200, height=25)

        Class_entry = tkinter.ttk.Combobox(player_detail_frame, font=('Times new roman', 15),
                                           textvariable=self.class_name,values=self.fetch_classes(),state='readonly',
                            )
        Class_entry.place(x=150, y=360, width=200, height=25)
        id_entry = Entry(player_detail_frame, font=('Times new Roman Bold', 15),textvariable=self.id_var,bg='lightyellow',state=DISABLED)
        id_entry.place(x=150,y=100)


        #--------------------------- BUTTONS ----------------------------------------------------------------------------------------------------#
        Save_btn = Button(player_detail_frame, text="Save",font=("Times New Roman", 15, 'bold'),command=self.save_data,
                          bg='lightblue', bd=2, relief=RIDGE)

        Save_btn.place(x=10, y=480, height=30, width=100)
        #
        Update_btn = Button(player_detail_frame, text="Update", font=("Times New Roman", 15, 'bold'),command=self.update,
                            bg='lightgreen', bd=2, relief=RIDGE)
        Update_btn.place(x=120,y=480, height=30, width=100)
        #
        Delete_btn = Button(player_detail_frame, text="Delete", font=("Times New Roman", 15, 'bold'),command=self.delete_data,
                            bg='red', bd=2, relief=RIDGE)
        Delete_btn.place(x=230,y=480 , height=30, width=100)
        clear_btn = Button(player_detail_frame, text="Clear", font=("Times New Roman", 15, 'bold'),bg='gray',bd=2, relief=RIDGE,command=self.clear)
        clear_btn.place(x=340, y=480, height=30, width=80)
        # add_wish=Button(player_detail_frame, text="Add Wish", font=("Times New Roman", 15, 'bold'),bg='lightgreen', bd=2)
        # add_wish.place(x=10,y=390,height=30, width=100)





        ######        VIEWING PLAYERS DETAILS OF RIGHT HAND SIDE OF THE SCREEN
        player_list_frame = Frame(self.root, bg="lightyellow", bd=2, relief=RIDGE)
        player_list_frame.place(x=550, y=140, width=520, height=300)

        scrolly = Scrollbar(player_list_frame, orient=VERTICAL)
        scrollx = Scrollbar(player_list_frame, orient=HORIZONTAL)
        #

        self.player_list_table = ttk.Treeview(player_list_frame, columns=("player_id","Username", "IG_tag","Class","Role in Raid","Role in Guild"),
                                              yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrolly.config(command=self.player_list_table.yview)
        scrollx.config(command=self.player_list_table.xview)
        self.player_list_table.heading("player_id", text='player id')
        self.player_list_table.heading("Username", text='Username')
        self.player_list_table.heading("IG_tag", text='IG_tag')
        self.player_list_table.heading("Role in Raid", text='Role in game')
        self.player_list_table.heading("Class",text='Class')
        self.player_list_table.heading("Role in Guild", text='Role in Guild')

        self.player_list_table.column("player_id", width=100)

        self.player_list_table.column('Username', width=120)
        self.player_list_table.column("IG_tag", width=100)
        self.player_list_table.column("Role in Guild", width=80)
        self.player_list_table.column("Role in Raid", width=100)
        self.player_list_table.column('Class',width=100)

        self.player_list_table.bind('<<TreeviewSelect>>', self.get_data)
        #
        # self.category_table.column("#0", stretch=NO, minwidth=0, width=0)  # Hide first default column or you can try code below

        self.player_list_table['show'] = 'headings'

        self.player_list_table.pack(fill=BOTH, expand=1)
        # self.supplier_table.bind('<<TreeviewSelect>>', self.get_data)

        #### SEARCH LABEL BY INVOICE NUMBER ON THE TOP RIGHT ##############

        Username_lbl = Label(self.root, text="Username", font=("Times New Roman", 15, 'bold'), bg='white').place(
            x=600, y=100)
        Username_entry = Entry(self.root, bg="lightyellow",textvariable=self.username_for_search,
                              font=("Times New Roman", 15, 'bold'), bd=2, relief=RIDGE).place(x=710, y=100, height=30,
                                                                                              width=150)

        search_button = Button(self.root, text="Search", font=("Times New Roman", 15, 'bold'),command=self.search,
                               bg='green')
        search_button.place(x=880, y=100, height=30, width=150)

        self.fetch_data()



    def fetch_data(self):
        self.player_list_table.delete(*self.player_list_table.get_children())
        conn = sqlite3.connect(resource_path('world_of_warcraft.db'))
        cur = conn.cursor()
        cur.execute('SELECT * FROM Players')
        rows = cur.fetchall()
        for row in rows:
            my_data=list(row)
            my_data.pop(2)
            print(my_data)



            self.player_list_table.insert("",END,values=my_data)


    def save_data(self):
        if self.IG_tag.get()!='' and self.Username.get()!='' and self.Role_in_guild.get()!='' and self.Role_in_raid.get()!='' and self.class_name.get()!='':
            try:
                conn = sqlite3.connect(resource_path('world_of_warcraft.db'))
                cur = conn.cursor()
            except:
                messagebox.showerror("Error", "Database connection failed",parent=self.root)

            else:
                cur.execute('SELECT * FROM Players WHERE in_game_tag=?',(self.IG_tag.get(),))
                rows = cur.fetchall()
                if len(rows)>0:
                    messagebox.showerror('Error','Player with same game tag already exists',parent=self.root)
                else:
                    password=simpledialog.askstring("Password_entry", "Enter your password", parent=self.root,show='*')
                    if password!='':
                        if len(password)>8:
                            try:
                                cur.execute('INSERT INTO players(Username,Password,in_game_tag,Class,Role_in_raid,Role_in_Guild) VALUES(?,?,?,?,?,?)',(self.Username.get(),password,self.IG_tag.get(),self.class_name.get(),self.Role_in_raid.get(),self.Role_in_guild.get(),))
                                conn.commit()
                                messagebox.showinfo("Successful","Player added successfully",parent=self.root)
                                self.fetch_data()
                            except Exception as e:
                                messagebox.showerror("Error",f"due to {e}",parent=self.root)
                        else:
                            messagebox.showerror("Error", "Password is too short",parent=self.root)

                    else:
                        messagebox.showerror("Error", "Password can't be empyty")
        else:
            messagebox.showerror("Error","Please enter all required fields",parent=self.root)



    def get_data(self, ev):
        selected_item = self.player_list_table.focus()  # Get the selected item in the Treeview
        if selected_item:  # Ensure an item is selected
            item_values = self.player_list_table.item(selected_item, 'values')  # Get the values of the selected item
            if item_values:  # Ensure values exist
                print(item_values)
                self.Username.set(item_values[1])
                self.Role_in_raid.set(item_values[4])
                self.IG_tag.set(item_values[2])
                self.Role_in_guild.set(item_values[5])
                self.class_name.set(item_values[3])
                self.id_var.set(item_values[0])



    def delete_data(self):
        conn=sqlite3.connect(resource_path('world_of_warcraft.db'))
        cursor=conn.cursor()
        try:
            cursor.execute('DELETE FROM players WHERE in_game_tag=?',(self.IG_tag.get(),))
            conn.commit()
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error",f"due to {e}",parent=self.root)


    def fetch_classes(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT Class from classes')
        rows=cursor.fetchall()
        return rows

    def search(self):

        if self.username_for_search.get()!='':
            data_to_search="%"+self.username_for_search.get() +"%"
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM players WHERE Username LIKE ?',(data_to_search,))
            rows=cursor.fetchall()
            self.player_list_table.delete(*self.player_list_table.get_children())
            for char in rows:
                self.player_list_table.insert('',END,values=char)

    def update(self):
        conn=connect_to_database()
        cursor=conn.cursor()

        cursor.execute('SELECT * FROM players WHERE Player_id=?',(self.id_var.get(),))
        rows=cursor.fetchall()
        if rows is None:
            messagebox.showerror("Error","No such player with that tag exists",parent=self.root)
        else:
            cursor.execute('Update players set Username=?,in_game_tag=?,Class=?,Role_in_raid=?,Role_in_Guild=? where Player_id=?',(self.Username.get(),self.IG_tag.get(),self.class_name.get(),self.Role_in_raid.get(),self.Role_in_guild.get(),self.id_var.get(),))
            conn.commit()
            messagebox.showinfo("Success","Updated successfully",parent=self.root)
            self.fetch_data()

    def clear(self):
        self.id_var.set('')
        self.username_for_search.set('')
        self.Username.set('')
        self.IG_tag.set('')
        self.class_name.set('')
        self.Role_in_raid.set('')
        self.Role_in_guild.set('')















if __name__ == "__main__":
    root=Tk()
    ProductClass(root)
    root.mainloop()