import logging
from time import sleep

from db import SessionLocal
from bot import controller as bot_controller
from scrapers import constants as scraper_constants
from scrapers.workers import ausbildung
from scrapers.models import ScrapingSession

logger = logging.getLogger(__name__)

MAPPER = {
    scraper_constants.Scrapers.ausbildung.value: ausbildung,
}


def get_worker(scraper):
    return MAPPER.get(scraper)


def run_worker(scraping_session):
    db = SessionLocal()
    try:
        worker = get_worker(scraping_session.scraper.value)
        worker.run(scraping_session)
    except Exception as e:
        scraping_session.status = scraper_constants.Statuses.failed
        db.add(scraping_session)
        db.commit()
        bot_controller.send_message(
            chat_id=scraping_session.user.telegram_id,
            text=f'Error occurred while scraping {scraping_session.scraper.value}.'
        )
        raise e
    else:
        scraping_session.status = scraper_constants.Statuses.ready
        db.add(scraping_session)
        db.commit()
        bot_controller.send_message(
            chat_id=scraping_session.user.telegram_id,
            text=f'Scraping {scraping_session.scraper.value} is done.'
        )


if __name__ == '__main__':
    while True:
        logger.info('Checking for pending sessions...')

        db = SessionLocal()

        pending_sessions = db.query(ScrapingSession).filter(
            ScrapingSession.status == scraper_constants.Statuses.pending
        ).all()

        for session in pending_sessions:
            logger.info(f'Running session {session.id}...')
            run_worker(session)

        db.close()
        # sleep(60 * 5)
