"""
Inspired by:
    - https://docs.python.org/3/library/sqlite3.html
"""
# In[] Libs
import sqlite3
import os

# In[] Inits
DB_ADDRESS = "database.db"
TABLE_NAME = "users"
db_connection = None

# In[] Functions
def init_db(db_address="", table_name=""):
    global db_connection
    # Check if the database already exists or not
    if os.path.exists(db_address):
        os.remove(db_address) # remove the database if already exists

    # Creating a Connection object that represents the database
    db_connection = sqlite3.connect(db_address) # The special path name :memory: can be provided to create a temporary database in RAM.

    # Create users table
    cur = db_connection.cursor()
    statement = f"""CREATE TABLE '{table_name}'
                    (fname text, lname text, gender text, age real)"""
    cur.execute(statement)

    db_connection.commit()

def add_user(table_name="", fname="", lname="", gender="", age=0):
    global db_connection
    cur = db_connection.cursor()    

    # Insert a row of data
    statement = f"""INSERT INTO '{table_name}'
                    VALUES
                        ('{fname}', '{lname}', '{gender}', {age})"""
    cur.execute(statement)

    db_connection.commit()

def show_data(table_name="", order_by=""):
    global db_connection
    cur = db_connection.cursor()
    statement = f"""SELECT * FROM '{table_name}'
                    ORDER BY '{order_by}'"""
    for row in cur.execute(statement):
        print(row)

# In[] App
if __name__ == "__main__":
    
    init_db(db_address=DB_ADDRESS, table_name=TABLE_NAME)
    add_user(table_name=TABLE_NAME, fname="Mustafa", lname="Sarshar", gender="male", age=33)
    add_user(table_name=TABLE_NAME, fname="Anna", lname="Zieger", gender="female", age=21)
    add_user(table_name=TABLE_NAME, fname="Yu", lname="Jang", gender="diverse", age=50)
    print("\nThese records are added to the database:\n")
    show_data(table_name=TABLE_NAME, order_by="fname")

    print("\nBye Bye!!!")
    db_connection.close()