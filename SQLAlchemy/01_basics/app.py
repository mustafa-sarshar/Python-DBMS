# In[] Libs
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# In[] Models
DB_Engine = None
Session = None
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
    username = Column(name="username", type_=String, unique=True, nullable=False)
    age = Column(name="age", type_=Integer, nullable=False)

# In[] Functions
def init_db(db_name=""):
    global DB_Engine, Session
    DB_Engine = create_engine(f"sqlite:///{db_name}", echo=True)
    Base.metadata.create_all(bind=DB_Engine)
    Session = sessionmaker(bind=DB_Engine)

def add_user(username="", age=0):    
    session = Session()
    user = User()
    user.username = username
    user.age = age
    session.add(user)
    try:
        session.commit()
    except Exception:
        print(f"The record for {username} could not be added!!!")
    session.close()

def update_user(search_exp=None, new_username=None, new_age=None):
    session = Session()

    user = session.query(User).filter(eval(search_exp)).first()
    if user:
        if new_username: user.username = new_username
        if new_age: user.age = new_age
    session.commit()
    session.close()

def delete_user(search_exp=None):
    session = Session()

    user = session.query(User).filter(eval(search_exp)).first()
    session.delete(user)
    session.commit()
    session.close()

def show_records(order_by=None, filter_by=None):
    session = Session()
    users = None
    if order_by: users = session.query(User).order_by(order_by)
    elif filter_by: users = session.query(User).filter(eval(filter_by)).all()
    else: users = session.query(User)
    print("\nThe records are:")
    for user in users:
        print("({}) - {}, {}".format(user.id, user.username, user.age))
    print("")

if __name__ == "__main__":
    init_db(db_name="database.db")

    add_user(username="mussar", age=30)
    add_user(username="bigboy", age=44)
    add_user(username="littlecutie", age=15)
    add_user(username="niceee", age=25)
    add_user(username="fakeuser", age=0)

    update_user(search_exp="User.username=='bigboy'", new_age=89)

    show_records()
    show_records(order_by=User.username)
    show_records(filter_by="User.username=='mussar'")
    show_records(filter_by="User.age>=30")

    delete_user(search_exp="User.username=='fakeuser'")
    show_records()

    print("ByeBye")