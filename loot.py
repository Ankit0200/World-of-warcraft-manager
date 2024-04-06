import os
import tkinter
import tkinter.ttk
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import ImageTk, Image
import ast
import sqlite3
import datetime
import sys
from tqdm import tk
import pandas as pd



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


class LootView:
    def __init__(self,root):
        self.root = root
        self.root.title("World of Warcraft Management")
        self.root.geometry("1100x580+260+130")
        # self.root.configure(background="#000025")

        self.label_title=Label(root,text="Loot management",font=("Arial",20,"bold"),fg="white",bg='green')
        self.label_title.place(x=0,y=0,relwidth=1,relheight=0.1)


        ##### VARIABLES =================
        self.loot_list=StringVar()
        self.class_name=StringVar()
        self.Boss_name=StringVar()

        self.class_name_for_search=StringVar()
        self.boss_name_for_search=StringVar()





        ### FRAMES AND VIEWS

        self.left_frame=Frame(self.root, bg="lightyellow", height=350, width=400, bd=5, relief=RIDGE)
        self.left_frame.place(x=50, y=150)
        self.Right_frame = Frame(self.root, bg="lightyellow", height=350, width=400, bd=5, relief=RIDGE)
        self.Right_frame.place(x=650, y=150)
        view_info_lbl = Label(self.root, text="View and modify", font=("Times New Roman", 20, "bold"), bg="green",
                              fg="white",
                              width=24, bd=2, relief=RIDGE)
        view_info_lbl.place(x=654, y=110)


        add_info_lbl=Label(self.root,text="Add info",font=("Times New Roman",20,"bold"),bg="green",fg="white",width=24,bd=2,relief=RIDGE)
        add_info_lbl.place(x=54,y=110)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        Loot_name=Label(self.left_frame, text="Loot:", font=("Times New Roman", 20, "bold"), bg="lightyellow")
        Loot_name.place(x=13,y=20)

        Boss_name=Label(self.left_frame, text="Boss:", font=("Times New Roman", 20, "bold"), bg="lightyellow")
        Boss_name.place(x=18,y=80)

        Class_name = Label(self.left_frame, text="Class:", font=("Times New Roman", 20, "bold"), bg="lightyellow")
        Class_name.place(x=10, y=130)

         ## ENTRIES TO ENTER ========================================
        loot_entry=Entry(self.left_frame, font=("Times New Roman", 15), width=20,textvariable=self.loot_list)
        loot_entry.place(x=100,y=29)


        Boss_entry =tkinter.ttk.Combobox(self.left_frame, font=("Times New Roman", 15), width=20, values=self.fetch_boss(), state="readonly",textvariable=self.Boss_name)
        Boss_entry.place(x=100, y=86)
        Boss_entry.current(0)
        class_entry = tkinter.ttk.Combobox(self.left_frame,textvariable=self.class_name, font=("Times New Roman", 15), width=20,values=self.fetch_class(), state="readonly")
        class_entry.place(x=100, y=140)
        class_entry.current(0)

        Add_Button=Button(self.left_frame, text="Add", font=("Times New Roman", 15), bg='green', fg='white',command=self.add)
        Add_Button.place(x=15,y=200,width=100)

        Warning_info=Label(self.left_frame, font=("Times New Roman", 16), bg="lightyellow", fg='red', text="Separate multiple lootname by comma")
        Warning_info.place(x=15,y=280)



        Boss_lbl_frame= LabelFrame(self.Right_frame,text='Boss',bg="lightyellow", font=("Times New Roman",15,'bold'),width=150, height=80)
        Boss_lbl_frame.place(x=9,y=14)

        Boss_combobox= ttk.Combobox(Boss_lbl_frame, values=self.fetch_boss(), font=("Times New Roman",15),width=10,textvariable=self.boss_name_for_search)
        Boss_combobox.place(x=10,y=10)
        Boss_combobox.current(0)

        Class_lbl_frame = LabelFrame(self.Right_frame, text='Class', bg="lightyellow",
                                    font=("Times New Roman", 15, 'bold'), width=150, height=80)
        Class_lbl_frame.place(x=220, y=14)

        Class_combobox = ttk.Combobox(Class_lbl_frame, values=self.fetch_class(), font=("Times New Roman", 15), width=10,textvariable=self.class_name_for_search)
        Class_combobox.place(x=10,y=10)
        Class_combobox.current(0)


        View_button=Button(self.Right_frame, text="View", font=("Times New Roman", 15, 'bold'), width=10,cursor='hand2',bg='skyblue',command=self.view_loot_by_select)
        View_button.place(x=120,y=110)


        #### LISTBOX ===============================
        Reward_viewing_frame = Frame(self.Right_frame, width=350, height=170, bg="green")

        Reward_viewing_frame.place(x=16, y=160)
        self.reward_list = Listbox(Reward_viewing_frame, font=("Times New Roman", 15, "bold"), bg="lightblue",
                                   relief=RIDGE, bd=2,width=35, height=7)

        scrolly_w = Scrollbar(Reward_viewing_frame, orient=VERTICAL, command=self.reward_list.yview)
        scrollx_w = Scrollbar(Reward_viewing_frame, orient=HORIZONTAL, command=self.reward_list.xview,width=4)

        self.reward_list.config(yscrollcommand=scrolly_w.set, xscrollcommand=scrollx_w.set)

        scrolly_w.pack(side=RIGHT, fill=Y)
        scrollx_w.pack(side=BOTTOM, fill=X)

        self.reward_list.pack(fill=BOTH, expand=True)

        delete_btn=Button(self.root, text="Delete", command=self.delete, relief=RIDGE,bg='#FF204E',font=("Times New Roman", 12, "bold"),fg='white')
        delete_btn.place(x=990,y=510)
        self.update_loot_in_boss_table()


    def fetch_boss(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT Boss_name FROM Boss')
        boss=cursor.fetchall()

        return [char[0] for char in boss]
    def fetch_class(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT Class FROM Classes')
        classes=cursor.fetchall()
        return [char[0] for char in classes]

    def add(self):
        if self.loot_list.get()=="" or self.class_name.get()=="" or self.Boss_name.get()=="":
            messagebox.showerror("Error", "Please enter all the fields")
        else:
            a=""
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM loots where Boss_name=? and Class=? ',(self.Boss_name.get(),self.class_name.get(),))

            datas=cursor.fetchall()

            if len(datas)==0:
                data=self.loot_list.get().split(',')
                for char in data:
                    a=a+ ","+char
                data_to_insert=a[1:]
                try:
                    cursor.execute('INSERT INTO loots(Loot_name,Boss_name,Class) VALUES (?,?,?)',(data_to_insert,self.Boss_name.get(),self.class_name.get()))
                    conn.commit()
                    messagebox.showinfo("Success", "Loot stored succcessfully",parent=self.root)
                    self.update_loot_in_boss_table()
                except Exception as e:
                    messagebox.showerror("Error",f"Error due to {e}",parent=self.root)
            else:
                received_data = self.loot_list.get().split(',')
                for char in received_data:
                    a = a + "," + char
                data_to_insert = a[1:]


                existing_data=datas[0][0]

                data_to_add=existing_data+","+data_to_insert



                cursor.execute('Update loots set Loot_name=? where Boss_name=? and Class=?',(data_to_add,self.Boss_name.get(),self.class_name.get(),))

                conn.commit()
                messagebox.showinfo("Successful","Loot stored succesfully",parent=self.root)

        self.view_loot_by_select()

    def view_loot_by_select(self):
        self.reward_list.delete(0,END)
        if self.boss_name_for_search.get()=="" or self.class_name_for_search.get()=="":
            messagebox.showerror("Error","Please select both boss and class",parent=self.root)
        else:
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute('SELECT * from loots where Boss_name=? and Class=?',(self.boss_name_for_search.get(),self.class_name_for_search.get(),))
            data=cursor.fetchone()
            if data is not None:
                data_to_view_in_list=data[0]
                for char in data_to_view_in_list.split(','):
                    self.reward_list.insert(END,char)
            else:
                messagebox.showinfo("Error","No data found",parent=self.root)

    def delete(self):
        try:
            index_ = self.reward_list.curselection()
            name = self.reward_list.get(index_)
        except IndexError:
            messagebox.showerror("Error",f"Please select item to delete",parent=self.root)
        else:
          is_sure=  messagebox.askokcancel("Warning",f"Do you sure want to delete {name} rewards ? ",parent=self.root)

          if is_sure:
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute('Select * from loots where Boss_name=? and Class=? ',(self.boss_name_for_search.get(),self.class_name_for_search.get(),))
            data_req=cursor.fetchone()
            if data_req is not None:
                loot_list=data_req[0].split(',')
                loot_list.remove(name)
                uff=str()
                print(loot_list)
                for char in loot_list:
                    uff=char+","+uff

                print(uff[:-1])

                cursor.execute('UPDATE loots SET Loot_name=? WHERE Boss_name=? and Class=?',(uff[:-1],self.boss_name_for_search.get(),self.class_name_for_search.get(),))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","You have successfully deleted the data",parent=self.root)
                self.update_loot_in_boss_table()

                self.view_loot_by_select()
            else:
                messagebox.showinfo("Error","Unidentified error. Please restart the app",parent=self.root)
          else:
              messagebox.showinfo("Message","Operation cancelled",parent=self.root)



    def update_loot_in_boss_table(self):

        conn = connect_to_database()  # Assuming you have a function to connect to the database
        cursor = conn.cursor()

        # Query to retrieve boss names and corresponding loot names
        query_loots = 'SELECT Boss_name, Loot_name FROM loots'

        # Read loot data into a DataFrame
        df_loots = pd.read_sql_query(query_loots, conn)

        # Group loot data by boss name and aggregate loot names into lists
        loots_by_boss = df_loots.groupby('Boss_name')['Loot_name'].agg(lambda x: ','.join(x)).reset_index()

        # Convert comma-separated loot names to lists
        loots_by_boss['Loot_name'] = loots_by_boss['Loot_name'].apply(lambda x: x.split(','))

        # Iterate over each boss and update the rewards column in the Boss_name table
        for boss, loot_list in zip(loots_by_boss['Boss_name'], loots_by_boss['Loot_name']):
            # Update rewards column for each boss
            update_query = f"UPDATE Boss SET rewards = ? WHERE Boss_name = ?"
            cursor.execute(update_query, (','.join(loot_list), boss))
            conn.commit()

        conn.close()


if __name__ == "__main__":
    root = Tk()
    LootView(root)
    root.mainloop()