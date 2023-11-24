import logging
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from requests_html import HTML, HTMLSession
from bs4 import BeautifulSoup, Tag

import config
from users.models import User
from scrapers.models import ScrapingSession, Record
from scrapers import utils as scraper_utils
from db import SessionLocal

logger = logging.getLogger(__name__)


class AbstractExplorePage:
    LOAD_MORE_BUTTON_XPATH = None
    EXPLORE_RESULTS_XPATH = None

    def __init__(self, url: str):
        self.driver = config.get_webdriver()
        self.url: str = url

    def render(self):
        self.driver.get(self.url)
        sleep(config.WAIT_TIME)
        self.accept_cookies()
        sleep(config.WAIT_TIME)

        found_links_count = 0
        failed_attempts = 0

        while True:
            self.scroll_bottom()

            sleep(config.WAIT_TIME)

            if found_links_count == len(self.found_links):
                try:
                    self.load_more_elements()
                except NoSuchElementException as e:
                    failed_attempts += 1
                    logger.info(f'Failed attempts: {failed_attempts}')
                    if failed_attempts == 3:
                        break
                    else:
                        continue
                else:
                    failed_attempts = 0

            found_links_count = len(self.found_links)

            logger.info(f'Found links: {found_links_count}')

    def accept_cookies(self):
        element = self.driver.find_element(By.XPATH, config.COOKIES_BUTTON_XPATH)
        element.click()

    def scroll_bottom(self):
        self.driver.execute_script(config.SCROLL_BOTTOM_SCRIPT)

    def load_more_elements(self):
        element = self.driver.find_element(by=By.XPATH, value=self.LOAD_MORE_BUTTON_XPATH)
        element.click()

    @property
    def explore_page_html(self):
        return HTML(html=self.driver.page_source, url=config.AUSBILDUNG_DE_BASE_URL)

    @property
    def explore_results(self):
        return self.explore_page_html.xpath(self.EXPLORE_RESULTS_XPATH, first=True)

    @property
    def found_links(self):
        return self.explore_results.absolute_links


class SearchPage(AbstractExplorePage):
    LOAD_MORE_BUTTON_XPATH = config.SEARCH_LOAD_MORE_BUTTON_XPATH
    EXPLORE_RESULTS_XPATH = config.SEARCH_RESULTS_XPATH


class JobsPage(AbstractExplorePage):
    LOAD_MORE_BUTTON_XPATH = config.JOB_LOAD_MORE_BUTTON_XPATH
    EXPLORE_RESULTS_XPATH = config.JOB_PAGE_RESULTS_XPATH

    def click_jobs_button(self, path='//*[@id="tab-bar-anchor"]/div/ul/li[2]/a'):
        self.driver.get(self.url)
        sleep(config.WAIT_TIME)
        self.accept_cookies()
        sleep(config.WAIT_TIME)
        element = self.driver.find_element(by=By.XPATH, value=path)
        element.click()

    def _load_more_elements(self, path='/html/body/div[3]/main/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div'):
        element = self.driver.find_element(by=By.XPATH, value=path)
        element.click()

    @property
    def _explore_results(self, path='/html/body/div[3]/main/div/div/div[1]/div/div[2]/div/div[2]/div'):
        return self.explore_page_html.xpath(path, first=True)

    @property
    def _found_links(self):
        return self._explore_results.absolute_links


class DetailPage:

    def __init__(self, url: str):
        self.url: str = url
        self.session: HTMLSession = HTMLSession()
        self._contact_div: Tag = Tag(name='div')
        self.has_contact_info = False

    def __del__(self):
        self.session.close()

    def render(self):
        response = self.session.get(self.url)

        soup = BeautifulSoup(response.html.html, 'html.parser')
        contact_div = soup.find("div", class_=config.CONTACT_DIV_CLASS)

        if contact_div:
            self._contact_div = contact_div
            self.has_contact_info = True

    @property
    def name(self):
        name_div = self._contact_div.find('div', class_=config.NAME_DIV_CLASS)
        return getattr(name_div, 'text', '').strip()

    @property
    def position(self):
        position_div = self._contact_div.find('div', class_=config.POSITION_DIV_CLASS)
        return getattr(position_div, 'text', '').strip()

    @property
    def email(self):
        email_div = self._contact_div.find('div', class_=config.EMAIL_DIV_CLASS)
        return getattr(email_div, 'text', '').strip()

    @property
    def phone(self):
        phone_div = self._contact_div.find('div', class_=config.PHONE_DIV_CLASS)
        return getattr(phone_div, 'text', '').strip()


def run(scraping_session: ScrapingSession):
    if scraper_utils.is_ausbildung_search_page(scraping_session.url):
        explore_page = SearchPage(scraping_session.url)
    elif scraper_utils.is_ausbildung_jobs_page(scraping_session.url):
        explore_page = JobsPage(scraping_session.url)
    else:
        raise ValueError('Invalid url.')

    try:
        explore_page.render()
        links = list(explore_page.found_links)
    except Exception as e:
        explore_page.driver.quit()
        raise e

    explore_page.driver.quit()

    with SessionLocal() as db:
        records_to_create = []

        for link in links:
            detail_page = DetailPage(link)
            detail_page.render()

            if any((detail_page.email, detail_page.phone)):
                record = Record(
                    url=link,
                    name=detail_page.name,
                    position=detail_page.position,
                    email=detail_page.email,
                    phone=detail_page.phone,
                    session_id=scraping_session.id
                )
                records_to_create.append(record)

            logger.info(f'{detail_page.name} - {detail_page.position} - {detail_page.email} - {detail_page.phone}')
            logger.info(f'{detail_page.url}')
            logger.info('---')

        db.bulk_save_objects(records_to_create)
        db.commit()
