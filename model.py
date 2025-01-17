from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import Union

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_table'
    id: Union[Column[int], int] = Column(Integer, primary_key=True)
    wins: Union[Column[int], int] = Column(Integer, nullable=False, default=0)
    total_games: Union[Column[int], int] = Column(Integer, nullable=False, default=0)
    secret_number: Union[Column[int], int] = Column(Integer, nullable=True, default=None)
    in_game: Union[Column[bool], bool] = Column(Boolean, nullable=False, default=False)
    attempts: Union[Column[int], int] = Column(Integer, nullable=False, default=0)
