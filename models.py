from sqlalchemy import Integer,Column,String,ForeignKey,Boolean
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key= True, index = True)
    username = Column(String,unique = True, index = True, nullable = True)
    hashedPassword = Column(String,nullable = False)
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key= True, index = True)
    title = Column(String,index = True,nullable = True)
    description = Column(String,nullable = True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User",back_populates="tasks")
    