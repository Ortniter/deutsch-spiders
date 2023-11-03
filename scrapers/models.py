from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import Enum as EnumColumn
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base
from scrapers import constants as scraper_constants


class ScrapingSession(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scraper = Column(EnumColumn(scraper_constants.Scrapers), index=True)
    url = Column(String, index=True)
    records = relationship('Record', back_populates='session')

    def __repr__(self) -> str:
        return f'<Session {self.scraper} - {self.created_at}>'

    def __str__(self) -> str:
        return f'{self.scraper} - {self.created_at}'


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    name = Column(String, index=True)
    position = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True)
    session_id = Column(Integer, ForeignKey('sessions.id', ondelete='CASCADE'))
    session = relationship('ScrapingSession', back_populates='records')

    def __repr__(self) -> str:
        return f'<Record {self.email}>'

    def __str__(self) -> str:
        return self.email
