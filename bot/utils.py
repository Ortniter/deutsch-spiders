import json
import datetime
from functools import cached_property

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import Actions
from users.models import User
from scrapers.models import ScrapingSession, Record
from scrapers.constants import Scrapers
from db import SessionLocal


def get_scrapers_keyboard():
    keyboard: list[list[InlineKeyboardButton]] = []

    for scraper in Scrapers:
        keyboard.append([
            InlineKeyboardButton(
                text=f'{scraper.value.capitalize()}',
                callback_data=json.dumps(
                    {
                        'action': Actions.LIST_SESSIONS.value,
                        'selected_scraper': scraper.value
                    }
                )
            )
        ])

    return InlineKeyboardMarkup(keyboard)


def get_sessions_keyboard(user):
    keyboard: list[list[InlineKeyboardButton]] = []

    sessions = user.sessions.filter(
        ScrapingSession.scraper == user.selected_scraper,
        ScrapingSession.created_at == datetime.date.today()
    ).all()

    for sessions in sessions:
        keyboard.append([
            InlineKeyboardButton(
                text=f'{sessions.formatted_status} {sessions.formatted_created_at}',
                callback_data=json.dumps({'action': Actions.LOAD_RECORDS.value, 'session_id': sessions.id})
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text='🔙',
            callback_data=json.dumps({'action': Actions.BACK.value, 'id': None})
        )
    ])

    return InlineKeyboardMarkup(keyboard)


class Mapper:

    def __init__(self, query_data, telegram_id):
        query_data = json.loads(query_data)
        self.selected_scraper = query_data.get('selected_scraper')
        self.telegram_id = telegram_id
        self.session_id = query_data.get('session_id')
        self.action = query_data['action']
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    @cached_property
    def current_user(self):
        return self.db.query(User).filter(User.telegram_id == self.telegram_id).first()

    @property
    def is_action_list_sessions(self):
        return self.action == Actions.LIST_SESSIONS.value

    @property
    def is_action_load_records(self):
        return self.action == Actions.LOAD_RECORDS.value

    @property
    def is_action_back(self):
        return self.action == Actions.BACK.value

    def get_selected_session(self):
        return self.db.query(ScrapingSession).filter(ScrapingSession.id == self.session_id).first()
