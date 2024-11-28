from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True)
    wins =  Column(Integer, nullable=False, default=0)
    total_games = Column(Integer, nullable=False, default=0)
    secret_number = Column(Integer, nullable=True, default=None)
    in_game = Column(Boolean, nullable=False, default=False)
    attempts = Column(Integer, nullable=False, default=0)
