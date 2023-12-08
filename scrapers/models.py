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
    status = Column(EnumColumn(scraper_constants.Statuses), index=True, default=scraper_constants.Statuses.pending)
    scraper = Column(EnumColumn(scraper_constants.Scrapers), index=True)
    url = Column(String, index=True)
    records = relationship('Record')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='sessions')

    def __repr__(self) -> str:
        return f'<Session {self.scraper} - {self.created_at}>'

    def __str__(self) -> str:
        return f'{self.scraper} - {self.created_at}'

    @property
    def is_ready(self):
        return self.status == scraper_constants.Statuses.ready

    @property
    def is_pending(self):
        return self.status == scraper_constants.Statuses.pending

    @property
    def is_failed(self):
        return self.status == scraper_constants.Statuses.failed

    @property
    def formatted_created_at(self):
        return self.created_at.strftime('%d/%m/%Y %H:%M:%S')

    @property
    def formatted_status(self):
        return self.status.value.capitalize()

    @property
    def summary(self):
        return (f'Status: {self.formatted_status}'
                f'\nCreated at: {self.formatted_created_at}'
                f'\nRecords: {len(self.records)}'
                f'\nScraper: {self.scraper.value}'
                f'\nUrl: {self.url}')

    @property
    def temp_file_config(self):
        return {
            'mode': 'w', 'delete': False, 'suffix': '.csv',
            'prefix': self.get_file_name_prefix(),
        }

    def get_file_name_prefix(self):
        return f'{self.scraper.value}_{self.created_at.strftime("%Y_%m_%d_%H_%M_%S")}'


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    name = Column(String, index=True, nullable=True)
    position = Column(String, index=True, nullable=True)
    email = Column(String, index=True)
    phone = Column(String, index=True, nullable=True)
    emails_from_description = Column(String, index=True, nullable=True)
    session_id = Column(Integer, ForeignKey('sessions.id', ondelete='CASCADE'))
    session = relationship('ScrapingSession', back_populates='records')

    def __repr__(self) -> str:
        return f'<Record {self.email}>'

    def __str__(self) -> str:
        return self.email
