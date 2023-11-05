from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship

from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=True)
    telegram_id = Column(Integer, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    # sessions = relationship('ScrapingSession', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return self.username

    @classmethod
    def create_or_update(cls, db: Session, **kwargs):
        user = db.query(cls).filter(cls.telegram_id == kwargs['telegram_id']).first()

        if not user:
            user = User(**kwargs)
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            user.username = kwargs['username']
            user.first_name = kwargs['first_name']
            user.last_name = kwargs['last_name']
            db.commit()

        return user

    @classmethod
    def get_by_telegram_id(cls, db: Session, telegram_id: int):
        return db.query(cls).filter(cls.telegram_id == telegram_id).first()
