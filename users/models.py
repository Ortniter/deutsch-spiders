from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=True)
    telegram_id = Column(Integer, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    sessions = relationship('ScrapingSession', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return self.username
