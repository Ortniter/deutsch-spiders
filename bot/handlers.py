import logging

from telegram import Update
from telegram.ext import ContextTypes

from db import SessionLocal
from bot import utils
from users.models import User
from scrapers.models import ScrapingSession, Record
from scrapers import utils as scraper_utils
from scrapers import constants as scraper_constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with SessionLocal() as db:
        User.create_or_update(
            db=db,
            username=update.effective_chat.username,
            telegram_id=update.effective_chat.id,
            first_name=update.effective_chat.first_name,
            last_name=update.effective_chat.last_name
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Let\'s scrape it all!'
    )


async def scrapers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Choose wisely:',
        reply_markup=utils.get_scrapers_keyboard()
    )


async def ausbildung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = ' '.join(context.args)

    if not url or not scraper_utils.is_valid_url(url):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Please provide a valid url.'
        )
        return

    with SessionLocal() as db:
        user = User.get_by_telegram_id(db=db, telegram_id=update.effective_chat.id)
        scraping_session = ScrapingSession(
            scraper=scraper_constants.Scrapers.ausbildung.value,
            url=url,
            user_id=user.id,
        )
        db.add(scraping_session)
        db.commit()
        db.refresh(scraping_session)

    logger.info(f'Starting scraping session: {scraping_session}')

    await scraper_utils.scrape(scraping_session)


class Button:

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        logger.info(query.data)

        self.data = utils.Mapper(query.data, query.message.chat_id)
        self.chat_id = query.message.chat_id
        self.previous_message_id = query.message.message_id
        self.bot = context.bot

        await self.process()

    async def process(self):
        if self.data.is_action_list_sessions:
            await self._list_sessions()

        elif self.data.is_action_load_records:
            await self._load_records()

        elif self.data.is_action_back:
            await self._back()

    async def _list_sessions(self, **kwargs):
        await self.bot.edit_message_reply_markup(
            chat_id=self.chat_id,
            message_id=self.previous_message_id,
            reply_markup=utils.get_sessions_keyboard(user=self.data.current_user),
        )

    async def _load_records(self, **kwargs):
        scraping_session = self.data.get_selected_session()

        if scraping_session.is_pending:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text='Session is pending. Please wait for it to finish.'
            )
        elif scraping_session.is_failed:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text='I am sorry, but this session has failed. Please try again later or contact the creator.'
            )
        else:
            file = scraper_utils.get_scraping_session_csv(scraping_session)
            await self.bot.send_document(
                chat_id=self.chat_id,
                document=file,
            )

    async def _back(self, **kwargs):
        await self.bot.edit_message_reply_markup(
            chat_id=self.chat_id,
            message_id=self.previous_message_id,
            reply_markup=utils.get_scrapers_keyboard(),
        )
