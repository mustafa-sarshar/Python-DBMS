# In[] Libs
import tkinter as tk
from tkinter import ttk, messagebox
import sqlalchemy as sql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.exc import SQLAlchemyError

# In[] Globals
DB_Engine = None
Session = None
Base = declarative_base()

# In[] Define Database Classes
# Association table
user_medications = sql.Table(
    "user_medications", Base.metadata, 
    sql.Column("user_id", sql.Integer, sql.ForeignKey("users.id"), primary_key=True),
    sql.Column("medication_id", sql.Integer, sql.ForeignKey("medications.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    fname = sql.Column(sql.String(length=50), nullable=False)
    lname = sql.Column(sql.String(length=50), nullable=False)
    age = sql.Column(sql.Integer, nullable=False)
    username = sql.Column(sql.String(length=125), nullable=False, unique=True)
    bio = sql.Column(sql.Text)
    # Many-to-one relationship - User<->Adress
    addresses = relationship(argument="Address", backref="users", cascade="all, delete, delete-orphan") # For many-to-one relationship Address.user, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.
    # Many-to-many relationship - User<->Medication
    medications = relationship(argument="Medication", secondary=user_medications, backref="users") # For a plain many-to-many, we use the un-mapped Table construct to serve as the association table.
    # medications = relationship(argument="Medication", secondary=user_medications)

    def __repr__(self):
        return f"({self.id}) - {self.fname} {self.lname}, {self.age} yr."

class Address(Base):
    __tablename__ = "addresses"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    email = sql.Column(sql.String(length=50), nullable=False)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    # user = relationship(argument="User", backref=backref(name="addresses", order_by=id), cascade="all, delete, delete-orphan", single_parent=True) # For many-to-one relationship Address.user, delete-orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship. To force this relationship to allow a particular "User" object to be referred towards by only a single "Address" object at a time via the Address.user relationship, which would allow delete-orphan cascade to take place in this direction, set the single_parent=True flag. (Background on this error at: https://sqlalche.me/e/14/bbf0)

    def __repr__(self):
        return f"{self.email} added to {self.user.username}"

class Medication(Base):
    __tablename__ = "medications"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    medication = sql.Column(sql.String(length=50), nullable=False, unique=True)
    # users = relationship(argument="User", secondary=user_medications)

    def __init__(self, medication):
        self.medication = medication
    
    def __repr__(self):
        return f"({self.id}) - {self.medication}"



# In[] Functions
def init_database():
    global DB_Engine, Session
    DB_Engine = create_engine(f"sqlite:///database.db", echo=True)
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
        self.frm_show_edit_users = ttk.Frame(master=self.tab_controller)
        self.frm_show_edit_users.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tab_controller.add(child=self.frm_add_user, text="Add user")
        self.tab_controller.add(child=self.frm_show_edit_users, text="Show/Edit user(s)")

        tab_add_user = AddUserTab(parent=self.frm_add_user)
        tab_show_edit_users = ShowEditUsersTab(parent=self.frm_show_edit_users)

class AddUserTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var_fname = tk.StringVar(master=parent, value="")
        self.var_lname = tk.StringVar(master=parent, value="")
        self.var_age = tk.IntVar(master=parent, value=0)
        self.var_bio = tk.StringVar(master=parent, value="biography here plz")
        self.addresses_list = []
        self.medications_list = []

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
        self.lbl_bio = ttk.Label(master=self.lbl_frm_1, text="Biography: ")
        self.lbl_bio.grid(row=3, column=0, sticky="E")
        self.ent_bio = ttk.Entry(master=self.lbl_frm_1, textvariable=self.var_bio)
        self.ent_bio.grid(row=4, columnspan=2, sticky="EWSN")

        self.btn_add_address = ttk.Button(master=self.lbl_frm_1, text="Add addresses", command=lambda: self.AddAddress(parent=self))
        self.btn_add_address.grid(row=5, columnspan=2, sticky="EW")
        self.btn_add_medication = ttk.Button(master=self.lbl_frm_1, text="Add medication", command=lambda: self.AddMedication(parent=self))
        self.btn_add_medication.grid(row=6, columnspan=2, sticky="EW")

        self.lbl_frm_2 = ttk.LabelFrame(master=parent)
        self.btn_add = ttk.Button(master=self.lbl_frm_2, text="Add", command=self.add_new_record)
        self.btn_add.grid(row=0, column=0, sticky="W")
        self.btn_reset = ttk.Button(master=self.lbl_frm_2, text="Reset", command=self.reset_widgets)
        self.btn_reset.grid(row=0, column=1, sticky="E")

        self.lbl_frm_1.grid(row=0, sticky="WENS")
        self.lbl_frm_2.grid(row=1, sticky="WENS")

        self.tkraise()

    class AddAddress(tk.Tk):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print(self, parent)
            self.parent = parent
            self.var_address = tk.StringVar(master=self, value="defaultname@mail.com")
            self.wm_title("Add a new address")
            self.geometry("200x70")
            
            self.lbl_address = ttk.Label(master=self, text="Enter the new address:")
            self.lbl_address.pack(fill=tk.BOTH, expand=True)
            self.ent_address = ttk.Entry(master=self, textvariable=self.var_address)
            self.ent_address.pack(fill=tk.BOTH, expand=True)
            self.btn_add = ttk.Button(master=self, text="Add", command=self.add_address)
            self.btn_add.pack(fill=tk.BOTH, expand=True)
        
        def add_address(self):
            if self.var_address.get():
                print(self.var_address.get())                
                self.parent.addresses_list.append(Address(email=self.var_address.get()))
                self.var_address.set("defaultname@mail.com")
                print(f"{len(self.parent.addresses_list)} addresses are added")

    class AddMedication(tk.Tk):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print(self, parent)
            self.parent = parent
            self.var_medication = tk.StringVar(master=self, value="medication")
            self.wm_title("Add a new medication")
            self.geometry("200x70")
            
            self.lbl_medication = ttk.Label(master=self, text="Enter the new medication:")
            self.lbl_medication.pack(fill=tk.BOTH, expand=True)
            self.ent_medication = ttk.Entry(master=self, textvariable=self.var_medication)
            self.ent_medication.pack(fill=tk.BOTH, expand=True)
            self.btn_add = ttk.Button(master=self, text="Add", command=self.add_medication)
            self.btn_add.pack(fill=tk.BOTH, expand=True)
        
        def add_medication(self):
            if self.var_medication.get():
                print(self.var_medication.get())                
                self.parent.medications_list.append(Medication(medication=self.var_medication.get()))
                self.var_medication.set("medication")
                print(f"{len(self.parent.medications_list)} medications are added")


    def add_new_record(self):
        session = Session()
        user = User()
        user.fname = self.var_fname.get()
        user.lname = self.var_lname.get()
        user.age = int(self.var_age.get())
        user.username = f"{user.fname.lower()}_{user.lname.lower()}_{user.age}"
        user.bio = self.var_bio.get()
        user.addresses = self.addresses_list
        # [Address(email="email_1@mail.com"), Address(email="email_2@mail.com"), Address(email="email_3@mail.com")]
        user.medications = self.medications_list

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
        self.var_bio.set(value="biography here plz")
        self.addresses_list = []
        self.medications_list = []

class ShowEditUsersTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lbl_users = ttk.Label(master=parent, text="All users:\n(id) - (username)", justify=tk.CENTER)
        self.lbl_users.grid(row=0, column=0, columnspan=2)
        self.lstbox_users = tk.Listbox(master=parent, selectmode=tk.MULTIPLE, width=50)
        self.lstbox_users.grid(row=1, column=0)
        self.scrollbar_users = ttk.Scrollbar(master=parent)
        self.scrollbar_users.grid(row=1, column=1)
        self.lstbox_users.config(yscrollcommand=self.scrollbar_users.set)
        self.scrollbar_users.config(command=self.lstbox_users.yview)
        self.btn_update_list = ttk.Button(master=parent, text="Update the list", command=self.update_list)
        self.btn_update_list.grid(row=2, column=0)
        self.btn_delete_record = ttk.Button(master=parent, text="Delete selected user", command=self.delete_record)
        self.btn_delete_record.grid(row=3, column=0)

    def update_list(self, order_by=None, filter_by=None):
        self.lstbox_users.delete(0, tk.END)
        session = Session()
        users = None
        if order_by: users = session.query(User).order_by(order_by)
        elif filter_by: users = session.query(User).filter(eval(filter_by)).all()
        else: users = session.query(User)
        print("\nThe records are:")
        for user in users:
            print(f"({user.id}) - {user.username}, {user.age}, {user.addresses[0].email}")
            self.lstbox_users.insert(tk.END, (f"{user.id})", "-", user.username))
        print("")        
        # users_list = [(f"({_user.id})", "-", _user.username) for _user in users]
        # self.lstbox_users.insert(0, *users_list)
        self.lbl_users.configure(text=f"All users (n={users.count()}):\n(id) - (username)")

        for u, a in session.query(User, Address).filter(User.id==Address.user_id).filter(Address.email=="asd@asd.com").all():
            print(f"User: {u}, email: {a.email}")
        session.close()

    def delete_record(self):
        session = Session()
        records_seleted = [self.lstbox_users.get(idx)[2] for idx in self.lstbox_users.curselection()]
        if len(records_seleted) > 0:
            for username in records_seleted:
                user = session.query(User).filter(User.username==username).first()
                session.delete(user)
            session.commit()
            self.update_list()

if __name__ == "__main__":
    init_database()
    app = App()
    app.mainloop()
