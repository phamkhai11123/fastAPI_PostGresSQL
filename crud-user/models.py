from sqlalchemy import String,Integer,Column
from database import Base,engine

def create_table():
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = '_user1_'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))

