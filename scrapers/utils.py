import csv
import multiprocessing
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile

from scrapers.workers import controller as scraper_controller


def get_scraping_session_csv(scraping_session):
    with NamedTemporaryFile(**scraping_session.temp_file_config) as csvfile:
        fieldnames = ['name', 'position', 'email', 'phone', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in scraping_session.records:
            writer.writerow(
                {
                    'name': record.name,
                    'position': record.position,
                    'email': record.email,
                    'phone': record.phone,
                    'url': record.url,
                }
            )

    return open(csvfile.name, 'rb')


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def scrape(scraping_session):
    scraper_controller.run_worker(scraping_session)
    # multiprocessing.Process(target=scraper_controller.run_worker, args=(scraping_session,)).start()
