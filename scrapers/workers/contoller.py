from db import SessionLocal
from bot import controller as bot_controller
from scrapers import constants as scraper_constants
from scrapers.workers import ausbildung
from scrapers.models import ScrapingSession

MAPPER = {
    scraper_constants.Scrapers.ausbildung.value: ausbildung,
}


def get_worker(scraper):
    return MAPPER.get(scraper)


def run_worker(session_id):
    db = SessionLocal()
    try:
        scraping_session = db.query(ScrapingSession).get(session_id)
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
