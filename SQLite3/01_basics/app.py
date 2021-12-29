"""
Inspired by:
    - https://docs.python.org/3/library/sqlite3.html
"""
# In[] Libs
import sqlite3

# In[] Inits
# Flags
GET_INFO = True
DB_ADDRESS = "database.db"
TABLE_NAME = "users"

# In[] Functions
def reset_db(db_address=""):
    import os
    if os.path.exists(db_address):
        os.remove(db_address)

def init_db(db_address="", table_name=""):
    # Creating a Connection object that represents the database
    con = sqlite3.connect(db_address) # The special path name :memory: can be provided to create a temporary database in RAM.

    # Create users table
    cur = con.cursor()
    statement = f"""CREATE TABLE '{table_name}'
                    (fname text, lname text, gender text, age real)"""
    cur.execute(statement)
    con.commit()
    con.close()

def add_user(db_address="", table_name="", fname="", lname="", gender="", age=0):
    con = sqlite3.connect(db_address)
    cur = con.cursor()    

    # Insert a row of data
    statement = f"""INSERT INTO '{table_name}'
                    VALUES
                        ('{fname}', '{lname}', '{gender}', {age})"""
    cur.execute(statement)
    con.commit()
    con.close()

def show_data(db_address="", table_name="", order_by=""):
    con = sqlite3.connect(db_address)
    cur = con.cursor()
    statement = f"""SELECT * FROM '{table_name}'
                    ORDER BY '{order_by}'"""
    for row in cur.execute(statement):
        print(row)
    con.close()

# In[] App
if __name__ == "__main__":
    reset_db(db_address=DB_ADDRESS)
    init_db(db_address=DB_ADDRESS, table_name=TABLE_NAME)
    add_user(db_address=DB_ADDRESS, table_name=TABLE_NAME, fname="Mustafa", lname="Sarshar", gender="male", age=33)
    add_user(db_address=DB_ADDRESS, table_name=TABLE_NAME, fname="Anna", lname="Zieger", gender="female", age=21)
    add_user(db_address=DB_ADDRESS, table_name=TABLE_NAME, fname="Yu", lname="Jang", gender="diverse", age=50)
    print("\nThese records are added to the database:\n")
    show_data(db_address=DB_ADDRESS, table_name=TABLE_NAME, order_by="fname")
    # while GET_INFO:
    #     pass

    print("\nBye Bye!!!")