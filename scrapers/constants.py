from enum import Enum


class Scrapers(str, Enum):
    ausbildung = 'ausbildung'


class Statuses(str, Enum):
    ready = 'ready'
    failed = 'failed'
    pending = 'pending'
