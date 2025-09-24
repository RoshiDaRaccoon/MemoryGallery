import enum
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Boolean, Float, Enum as SQLEnum
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hashed = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    
    refresh_token = Column(String, nullable=True)
    
    def __repr__(self):
        return f"User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"
    