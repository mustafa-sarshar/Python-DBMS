# In[] Libs
import tkinter as tk
from tkinter import ttk, messagebox
import sqlalchemy as sql
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# In[] Globals
DB_Engine = None
Session = None
Base = declarative_base()

# In[] Define Database Classes
class User(Base):
    __tablename__ = "user"

    id = sql.Column(name="id", type_=sql.Integer, primary_key=True, autoincrement=True)
    fname = sql.Column(name="fname", type_=sql.String(length=50), nullable=False)
    lname = sql.Column(name="lname", type_=sql.String(length=50), nullable=False)
    age = sql.Column(name="age", type_=sql.Integer, nullable=False)
    username = sql.Column(name="username", type_=sql.String(length=125), nullable=False, unique=True)

    def __repr__(self):
        return f"({self.id}) - {self.fname} {self.lname}, {self.age} yr."

# In[] Functions
def init_database():
    global DB_Engine, Session
    DB_Engine = create_engine(f"sqlite:///database.db", echo=False)
    Base.metadata.create_all(bind=DB_Engine)
    Session = sessionmaker(bind=DB_Engine)

# In[] Layout Classes
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wm_title("Main App")
        self.geometry("400x300")

        self._init_frames()
        # self.protocol("WM_DELETE_WINDOW", self.on_closing_app)

    def _init_frames(self):
        self.tab_controller = ttk.Notebook(master=self)
        self.tab_controller.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frm_add_user = ttk.Frame(master=self.tab_controller)
        self.frm_add_user.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frm_update_user = ttk.Frame(master=self.tab_controller)
        self.frm_update_user.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frm_delete_user = ttk.Frame(master=self.tab_controller)
        self.frm_delete_user.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frm_show_users = ttk.Frame(master=self.tab_controller)
        self.frm_show_users.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tab_controller.add(child=self.frm_add_user, text="Add user")
        self.tab_controller.add(child=self.frm_update_user, text="Update user(s)")
        self.tab_controller.add(child=self.frm_delete_user, text="Delete user(s)")
        self.tab_controller.add(child=self.frm_show_users, text="Show user(s)")

        tab_add_user = AddUserTab(parent=self.frm_add_user)
        tab_update_user = UpdateUserTab(parent=self.frm_update_user)
        tab_show_users = ShowUsersTab(parent=self.frm_show_users)

class AddUserTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.var_fname = tk.StringVar(master=parent, value="")
        self.var_lname = tk.StringVar(master=parent, value="")
        self.var_age = tk.IntVar(master=parent, value=0)

        self.lbl_frm_1 = ttk.LabelFrame(master=parent)
        self.lbl_fname = ttk.Label(master=self.lbl_frm_1, text="First name: ")
        self.lbl_fname.grid(row=0, column=0, sticky="E")
        self.ent_fname = ttk.Entry(master=self.lbl_frm_1, textvariable=self.var_fname)
        self.ent_fname.grid(row=0, column=1, sticky="W")
        self.lbl_lname = ttk.Label(master=self.lbl_frm_1, text="Last name: ")
        self.lbl_lname.grid(row=1, column=0, sticky="E")
        self.ent_lname = ttk.Entry(master=self.lbl_frm_1, textvariable=self.var_lname)
        self.ent_lname.grid(row=1, column=1, sticky="W")
        self.lbl_age = ttk.Label(master=self.lbl_frm_1, text="Age: ")
        self.lbl_age.grid(row=2, column=0, sticky="E")
        self.ent_age = ttk.Entry(master=self.lbl_frm_1, textvariable=self.var_age)
        self.ent_age.grid(row=2, column=1, sticky="W")

        self.lbl_frm_2 = ttk.LabelFrame(master=parent)
        self.btn_add = ttk.Button(master=self.lbl_frm_2, text="Add", command=self.add_new_record)
        self.btn_add.grid(row=3, column=0)
        self.btn_reset = ttk.Button(master=self.lbl_frm_2, text="Reset", command=self.reset_widgets)
        self.btn_reset.grid(row=3, column=1)

        self.lbl_frm_1.grid(row=0, sticky="WENS")
        self.lbl_frm_2.grid(row=1, sticky="WENS")

        self.tkraise()

    def add_new_record(self):
        session = Session()
        user = User()
        user.fname = self.var_fname.get()
        user.lname = self.var_lname.get()
        user.age = int(self.var_age.get())
        user.username = f"{user.fname.lower()}_{user.lname.lower()}_{user.age}"

        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError as err:
            print(f"The record could not be added!!!")
            print("Error:", err)
            messagebox.showerror(title=f"Error: {err.code}", message=err.args)
        finally:
            session.close()
            self.reset_widgets()
    
    def reset_widgets(self):
        self.var_fname.set(value="")
        self.var_lname.set(value="")
        self.var_age.set(value=0)

class UpdateUserTab(AddUserTab):
    pass

class ShowUsersTab(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.lbl_users = ttk.Label(master=parent, text="All users:\n(id) - (username)", justify=tk.CENTER)
        self.lbl_users.grid(row=0, column=0, columnspan=2)
        self.lstbox_users = tk.Listbox(master=parent, selectmode=tk.MULTIPLE, width=50)
        self.lstbox_users.grid(row=1, column=0)
        self.scrollbar_users = ttk.Scrollbar(master=parent)
        self.scrollbar_users.grid(row=1, column=1)
        self.lstbox_users.config(yscrollcommand=self.scrollbar_users.set)
        self.scrollbar_users.config(command=self.lstbox_users.yview)
        self.btn_update_list = ttk.Button(master=parent, text="Update the list", command=self.update_list)
        self.btn_update_list.grid(row=2, columnspan=2)

    def update_list(self, order_by=None, filter_by=None):
        session = Session()
        users = None
        if order_by: users = session.query(User).order_by(order_by)
        elif filter_by: users = session.query(User).filter(eval(filter_by)).all()
        else: users = session.query(User)
        print("\nThe records are:")
        for user in users:
            print("({user.id}) - {user.username}, {user.age}")
        print("")        
        users_list = [(f"({_user.id})", "-", _user.username) for _user in users]
        self.lstbox_users.insert(0, *users_list)  

if __name__ == "__main__":
    init_database()
    app = App()
    app.mainloop()
