import csv
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile


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


def is_ausbildung_search_page(url):
    return 'suche' in url


def is_ausbildung_jobs_page(url):
    return 'berufe' in url
