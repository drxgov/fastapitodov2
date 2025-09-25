from sqlalchemy import Integer,Column,String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key= True, index = True)
    username = Column(String,unique = True, index = True, nullable = True)
    hashedPassword = Column(String,nullable = False)