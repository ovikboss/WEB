from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from sqlalchemy import create_engine
engine = create_engine("sqlite:///Users.db")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password:Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    phone_number :Mapped[str]
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str]
    coment: Mapped[str]
    name:Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="contacts")
    def __repr__(self) -> str:
        return f"Contact:(id={self.id!r}, Номер телефона={self.phone_number!r}, Комментарий={self.coment!r})"

Base.metadata.create_all(engine)

def new_user(Name: str, Full_name: str, Phone_number: str, Passw:str ):
        with Session(engine) as session:
            user = User(name = Name,fullname = Full_name, phone_number = Phone_number ,password = Passw)
            session.add_all([user])
            session.commit()
            return user.id

def new_conntact(Name: str, Phone_number: str, Coment:str , ID:int):
        with Session(engine) as session:
            stmt = select(User).where(User.id.in_([ID]))
            for user in session.scalars(stmt):
                user.contacts.append(Contact(name = Name, phone_number = Phone_number ,coment = Coment, user_id = ID))
            session.add_all([user])
            session.commit()

def check_pass_log(login ,password):
     with Session(engine) as session:
            stmt = select(User).where(User.name.in_([login]))
            for user in session.scalars(stmt):
                if user :
                    if password ==  user.password:
                        return True
                 
            return False
     
def check_log(login ):
     with Session(engine) as session:
            stmt = select(User).where(User.name.in_([login]))
            for user in session.scalars(stmt):
                if user.name == login:
                        return True
                 
            return False
     
def select_contacts(ID):
     data = []
     print(ID)
     with Session(engine) as session:   
        stmt = select(Contact).where(Contact.user_id == ID)
        for cont in session.scalars(stmt):
            data.append({"ID":cont.id,"Name":cont.name,"Phonenum":cont.phone_number,"Coment":cont.coment})
        print(data)
        return data
    
def select_num(name):
    with Session(engine) as session:
        stmt = select(User).where(User.name == name)
        for user in session.scalars(stmt):
             return user.phone_number, user.id

        

          

     
                