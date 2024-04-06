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


class Wishlist_view:
    def __init__(self,root):
        self.root = root
        self.root.title("World of Warcraft Management")
        self.root.geometry("1100x680+260+90")
        # self.root.configure(background="#000025")

        self.label_title=Label(root,text="Wishlist Management",font=("Arial",20,"bold"),fg="white",bg='green')
        self.label_title.place(x=0,y=0,relwidth=1,relheight=0.1)


        ##### VARIABLES =================
        self.IG_tag=StringVar()
        self.class_name=StringVar()
        self.Boss_name=StringVar()

        self.class_name_for_search=StringVar()
        self.Ig_tag_for_search=StringVar()


        ### FRAMES AND VIEWS

        self.left_frame=Frame(self.root, bg="lightyellow", height=350, width=450, bd=5, relief=RIDGE)
        self.left_frame.place(x=50, y=150,height=500)
        self.Right_frame = Frame(self.root, bg="lightyellow", height=495, width=400, bd=5, relief=RIDGE)
        self.Right_frame.place(x=650, y=150)
        view_info_lbl = Label(self.root, text="View and modify", font=("Times New Roman", 20, "bold"), bg="green",
                              fg="white",
                              width=24, bd=2, relief=RIDGE)
        view_info_lbl.place(x=654, y=110)


        add_info_lbl=Label(self.root,text="Add info",font=("Times New Roman",20,"bold"),bg="green",fg="white",width=27,bd=2,relief=RIDGE)
        add_info_lbl.place(x=54,y=110)

        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        IG_tag=Label(self.left_frame, text="IG Tag:", font=("Times New Roman", 20, "bold"), bg="lightyellow")
        IG_tag.place(x=13,y=20)

        Boss_name=Label(self.left_frame, text="Boss:", font=("Times New Roman", 20, "bold"), bg="lightyellow")
        Boss_name.place(x=18,y=80)

        Reward_name = Label(self.left_frame, text="Rewards", font=("Times New Roman", 20, "bold"), bg="lightyellow")
        Reward_name.place(x=10, y=130)

         ## ENTRIES TO ENTER ========================================
        self.IG_entry=tkinter.ttk.Combobox(self.left_frame, font=("Times New Roman", 15), width=20, textvariable=self.IG_tag,state="readonly",values=self.fetch_IG_tag())
        self.IG_entry.place(x=150,y=29)

        self.Boss_entry =tkinter.ttk.Combobox(self.left_frame, font=("Times New Roman", 15), width=20, values=self.fetch_boss(), state="readonly",textvariable=self.Boss_name)
        self.Boss_entry.place(x=150, y=86)
        self.Boss_entry.current(0)

        Reward_viewing_frame_left = Frame(self.left_frame, width=25, height=170, bg="green")

        Reward_viewing_frame_left.place(x=150, y=145)

        self.reward_list_left = Listbox(Reward_viewing_frame_left, font=("Times New Roman", 15, "bold"), bg="pink",
                                        relief=RIDGE, bd=2, width=25, height=7,selectmode=MULTIPLE)

        scrolly_w_left = Scrollbar(Reward_viewing_frame_left, orient=VERTICAL, command=self.reward_list_left.yview)
        scrollx_w_left = Scrollbar(Reward_viewing_frame_left, orient=HORIZONTAL, command=self.reward_list_left.xview, width=4)

        self.reward_list_left.config(yscrollcommand=scrolly_w_left.set, xscrollcommand=scrollx_w_left.set)

        scrolly_w_left.pack(side=RIGHT, fill=Y)
        scrollx_w_left.pack(side=BOTTOM, fill=X)

        self.reward_list_left.pack(fill=BOTH, expand=True)

        self.reward_list_left.bind("<<ListboxSelect>>", self.on_select_left)


        Selected_reward=Label(self.left_frame,text="Selected:",font=("Times New Roman",20,"bold"),bg='lightyellow')
        Selected_reward.place(x=10,y=350)

        self.view_selected_reward=Text(self.left_frame,width=25,height=5,bg='skyblue',fg='black',font=("Times New Roman",14,'bold',),state=NORMAL)
        self.view_selected_reward.place(x=150,y=360)


        Add_Button=Button(self.left_frame, text="Add", font=("Times New Roman", 15), bg='green', fg='white',command=self.add)

        Add_Button.place(x=20,y=300,width=80)



        #==========================================================================================================================


        IG_tag_lbl_frame_right= LabelFrame(self.Right_frame,text='IG_tag',bg="lightyellow", font=("Times New Roman",15,'bold'),width=350, height=80)
        IG_tag_lbl_frame_right.place(x=19,y=14)

        self.Right_IG_tag_combobox= ttk.Combobox(IG_tag_lbl_frame_right, values=self.fetch_IG_tag(), font=("Times New Roman",15), width=30, textvariable=self.Ig_tag_for_search)
        self.Right_IG_tag_combobox.place(x=14,y=10)
        self.Right_IG_tag_combobox.current(0)

        if len(sys.argv) > 1:
            print(sys.argv[1])
            if sys.argv[1] in self.fetch_IG_tag():
                self.IG_entry.set(sys.argv[1])
                self.IG_entry.config(state='disabled')





        #### LISTBOX ===============================
        Right_wishlist_viewing_frame = Frame(self.Right_frame, width=350, height=170, bg="green")

        Right_wishlist_viewing_frame.place(x=16, y=160)
        self.individual_wish_list = Listbox(Right_wishlist_viewing_frame, font=("Times New Roman", 15, "bold"), bg="lightblue",
                                            relief=RIDGE, bd=2, width=35, height=7)

        scrolly_w = Scrollbar(Right_wishlist_viewing_frame, orient=VERTICAL, command=self.individual_wish_list.yview)
        scrollx_w = Scrollbar(Right_wishlist_viewing_frame, orient=HORIZONTAL, command=self.individual_wish_list.xview, width=4)

        self.individual_wish_list.config(yscrollcommand=scrolly_w.set, xscrollcommand=scrollx_w.set)

        scrolly_w.pack(side=RIGHT, fill=Y)
        scrollx_w.pack(side=BOTTOM, fill=X)

        self.individual_wish_list.pack(fill=BOTH, expand=True)


        delete_btn=Button(self.root, text="Delete", relief=RIDGE,bg='#FF204E',font=("Times New Roman", 12, "bold"),fg='white',command=self.delete_wish)
        delete_btn.place(x=950,y=510)

        self.IG_entry.bind("<<ComboboxSelected>>", self.update_rewards)
        self.Boss_entry.bind("<<ComboboxSelected>>", self.update_rewards)
        self.Right_IG_tag_combobox.bind("<<ComboboxSelected>>", self.view_my_wishlist)

    def fetch_boss(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT Boss_name FROM Boss')
        boss=cursor.fetchall()
        return [each_boss[0] for each_boss in boss]

    def on_select_left(self,ev):
        values=[self.reward_list_left.get(idx) for idx in self.reward_list_left.curselection()]

        self.view_selected_reward.delete(1.0,END)
        for value in values:
            self.view_selected_reward.insert(END,value+'\n')



    def fetch_IG_tag(self):
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT in_game_tag FROM Players')
        rows=cursor.fetchall()
        return [row[0] for row in rows]


    def fetch_available_rewards(self):

        pass

    def update_rewards(self,ev):

        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT Class FROM Players where in_game_tag=?', (self.IG_tag.get(),))
        row=cursor.fetchone()
        try:
            Class_required=row[0]
        except:
            messagebox.showerror("Error","Database error !  ",parent=self.root)

        if Class_required!='':

            cursor.execute('Select Loot_name from loots where Class=? and Boss_name=?', (Class_required,self.Boss_name.get(),))
            datas=cursor.fetchone()


            self.reward_list_left.delete(0, END)
            try:
                data=datas[0]
                list_reward=data.split(',')
            except:

                pass
            else:


                for char in list_reward:
                        self.reward_list_left.insert(END,char)

    def add(self):

        values = [self.reward_list_left.get(idx) for idx in self.reward_list_left.curselection()]
        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('Select Wishlist from wishlist where Ig_tag=?', (self.IG_tag.get(),))
        row=cursor.fetchone()
        if row is None:
            my_list_without_empty_strings = [item for item in values if item != ""]
            selected_values_str = ','.join(my_list_without_empty_strings)
            cursor.execute('INSERT INTO wishlist (Ig_tag,Wishlist) VALUES (?,?)', (self.IG_tag.get(), selected_values_str),)
            conn.commit()
            messagebox.showinfo("Success","Successfully added",parent=self.root)
        else:
            current_value=','.join(values)
            print(current_value)
            value_to_add=row[0]+','+current_value
            cursor.execute('UPDATE wishlist set Wishlist=? where Ig_tag=?', (value_to_add,self.IG_tag.get(),))
            conn.commit()
            messagebox.showinfo('Succeed',"Added successfully!",parent=self.root)
            self.view_my_wishlist(ev=NONE)


    def view_my_wishlist(self,ev):
        print("Hello loop arrived here once")
        self.individual_wish_list.delete(0,END)

        conn=connect_to_database()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM wishlist where Ig_tag=?', (self.Ig_tag_for_search.get(),))
        row=cursor.fetchone()
        if row is not None:
            print(row)
            my_list=list(row)
            print(my_list[1].split(','))
            data_to_show=my_list[1].split(',')
            for char in data_to_show:
                if char!='':
                    self.individual_wish_list.insert(END,char)


    def delete_wish(self):
        try:
            # Get the index of the selected item
            index_ = self.individual_wish_list.curselection()
            print(index_)
        except:
            index_ = None
        if not index_:
            messagebox.showinfo('Error', 'Please select the value to delete first', parent=self.root)
        else:
            # Get the actual value to delete
            actual_value_to_delete = self.individual_wish_list.get(index_)
            conn=connect_to_database()
            cursor=conn.cursor()
            cursor.execute('SELECT Wishlist FROM wishlist WHERE Ig_tag=?', (self.Ig_tag_for_search.get(),))
            rows=cursor.fetchone()
            print(rows)
            my_list=rows[0]
            listed_data=my_list.split(',')
            listed_data.remove(actual_value_to_delete)
            listed_data=','.join(listed_data)
            cursor.execute('UPDATE wishlist SET Wishlist=? WHERE Ig_tag=?',(listed_data,self.Ig_tag_for_search.get(),))
            conn.commit()
            self.view_my_wishlist(ev=None)
            self.on_select_left(ev=None)




if __name__ == "__main__":
    root = Tk()
    Wishlist_view(root)
    root.mainloop()