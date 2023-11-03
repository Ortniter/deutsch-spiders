import logging
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from requests_html import HTML, HTMLSession
from bs4 import BeautifulSoup, Tag

import config

logger = logging.getLogger(__name__)


class SearchPage:
    def __init__(self, search_page: str = None):
        self.driver: WebDriver = webdriver.Chrome(
            service=config.get_chrome_service(),
            options=config.get_chrome_options()
        )
        self.search_page = search_page or config.SEARCH_PAGE
        self.session: HTMLSession = HTMLSession()

    def render(self):
        self.driver.get(self.search_page)
        sleep(3)
        self.accept_cookies()
        sleep(1)

        found_links_count = 0

        while True:
            self.scroll_bottom()

            sleep(1)

            if found_links_count == len(self.found_links):
                try:
                    self.load_more_elements()
                except NoSuchElementException as e:
                    break

            found_links_count = len(self.found_links)

            print(f'Found links: {found_links_count}')

    def accept_cookies(self):
        element = self.driver.find_element(By.XPATH, config.COOKIES_BUTTON_XPATH)
        element.click()

    def scroll_bottom(self):
        self.driver.execute_script(config.SCROLL_BOTTOM_SCRIPT)

    def load_more_elements(self):
        element = self.driver.find_element(by=By.XPATH, value=config.LOAD_MORE_BUTTON_XPATH)
        element.click()

    @property
    def search_page_html(self):
        return HTML(html=self.driver.page_source, url=config.AUSBILDUNG_DE_BASE_URL)

    @property
    def search_results(self):
        return self.search_page_html.xpath(config.SEARCH_RESULTS_XPATH, first=True)

    @property
    def found_links(self):
        return self.search_results.absolute_links


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
        response.html.render(sleep=1, keep_page=True, scrolldown=1)

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


def run():
    search_page = SearchPage()
    search_page.render()

    links = list(search_page.found_links)

    for link in links:
        detail_page = DetailPage(link)
        detail_page.render()
        print(f'{detail_page.name} - {detail_page.position} - {detail_page.email} - {detail_page.phone}')
        print(f'{detail_page.url}')
        print('---')


if __name__ == '__main__':
    run()
