"""
Inspired by:
    - https://docs.python.org/3/library/sqlite3.html
"""
# In[] Libs
import sqlite3

# In[] Inits
# Flags
GET_INFO = True

# Creating a Connection object that represents the database
con = sqlite3.connect("database.db") # The special path name :memory: can be provided to create a temporary database in RAM.
# Once a Connection has been established, create a Cursor object and call its execute() method to perform SQL commands
cur = con.cursor()

# Create table
cur.execute('''
    CREATE TABLE stocks (
        fname text,
        lname text,
        gender text,
        age real,
    )
''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

# In[] App
if __name__ == "__main__":
    while GET_INFO:
        pass

    print("Bye Bye!!!")