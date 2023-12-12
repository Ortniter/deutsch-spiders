import json
import datetime
from functools import cached_property

from sqlalchemy import Date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import Actions, SCRAPERS_TO_PAGES
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


def get_sessions_keyboard(user, scraper, page_number=1):
    keyboard: list[list[InlineKeyboardButton]] = []

    sessions = user.sessions.filter(
        ScrapingSession.scraper == scraper,
        ScrapingSession.created_at.cast(Date) == datetime.date.today()
    ).all()
    paginator = Paginator(sessions, page_number=page_number)

    for session in paginator.current_page:
        keyboard.append([
            InlineKeyboardButton(
                text=f'{session.formatted_status} {session.formatted_created_at}',
                callback_data=json.dumps({'action': Actions.GET_SUMMARY.value, 'session_id': session.id})
            )
        ])
        keyboard.append([
            InlineKeyboardButton(
                text='🤖 CSV',
                callback_data=json.dumps({'action': Actions.LOAD_RECORDS.value, 'session_id': session.id})
            ),
            InlineKeyboardButton(
                text='👁 LINK',
                url=session.url,
            )
        ])

    if paginator.has_pages:
        pagination_block = list()

        if not paginator.is_the_first_page:
            pagination_block.append(
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data=json.dumps(
                        {
                            'action': SCRAPERS_TO_PAGES[scraper],
                            'page_number': paginator.previous_page_number,
                        }
                    )
                )
            )

        pagination_block.append(
            InlineKeyboardButton(
                text=f'{paginator.page_number}/{paginator.pages_count}',
                callback_data=json.dumps(
                    {
                        'action': SCRAPERS_TO_PAGES[scraper],
                        'page_number': paginator.page_number,
                    }
                )
            )
        )

        if not paginator.is_the_last_page:
            pagination_block.append(
                InlineKeyboardButton(
                    text='➡️',
                    callback_data=json.dumps(
                        {
                            'action': SCRAPERS_TO_PAGES[scraper],
                            'page_number': paginator.next_page_number,
                        }
                    )
                )
            )

        keyboard.append(pagination_block)

    keyboard.append([
        InlineKeyboardButton(
            text='🔙',
            callback_data=json.dumps({'action': Actions.BACK.value, 'id': None})
        )
    ])

    return InlineKeyboardMarkup(keyboard)


class Paginator:

    def __init__(self, object_list, page_size=10, page_number=1):
        self.object_list = object_list
        self.page_size = page_size
        self.page_number = page_number

    @cached_property
    def pages(self):
        pages = [self.object_list[i:i + self.page_size] for i in range(0, len(self.object_list), self.page_size)]
        return {
            page_number: page
            for page_number, page in enumerate(pages, start=1)
        }

    @property
    def has_pages(self):
        return len(self.pages) > 1

    @property
    def pages_count(self):
        return len(self.pages)

    @property
    def current_page(self):
        return self.pages.get(self.page_number, [])

    @property
    def is_the_first_page(self):
        return self.page_number == 1

    @property
    def is_the_last_page(self):
        return self.page_number == self.pages_count

    @property
    def next_page_number(self):
        return self.validate_number(self.page_number + 1)

    @property
    def previous_page_number(self):
        return self.validate_number(self.page_number - 1)

    def validate_number(self, number):
        if number < 1:
            return 1
        elif number > self.pages_count:
            return self.pages_count
        else:
            return number


class Mapper:

    def __init__(self, query_data, telegram_id):
        query_data = json.loads(query_data)
        self.selected_scraper = query_data.get('selected_scraper')
        self.telegram_id = telegram_id
        self.session_id = query_data.get('session_id')
        self.page_number = query_data.get('page_number')
        self.action = query_data['action']
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    @cached_property
    def current_user(self):
        return self.db.query(User).filter(User.telegram_id == self.telegram_id).first()

    @property
    def is_action_get_summary(self):
        return self.action == Actions.GET_SUMMARY.value

    @property
    def is_action_list_sessions(self):
        return self.action == Actions.LIST_SESSIONS.value

    @property
    def is_action_ausbildung_page(self):
        return self.action == Actions.AUSBILDUNG_PAGE.value

    @property
    def is_action_load_records(self):
        return self.action == Actions.LOAD_RECORDS.value

    @property
    def is_action_back(self):
        return self.action == Actions.BACK.value

    def get_selected_session(self):
        return self.db.query(ScrapingSession).filter(ScrapingSession.id == self.session_id).first()
