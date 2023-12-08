from decouple import config as decouple_config
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

# Database
DATABASE_URL = decouple_config('DATABASE_URL', 'sqlite:///./sql_app.db', cast=str)
POSTGRES_HOST = decouple_config('POSTGRES_HOST', '', cast=str)
POSTGRES_PORT = decouple_config('POSTGRES_PORT', '', cast=str)
POSTGRES_DB = decouple_config('POSTGRES_DB', '', cast=str)
POSTGRES_USER = decouple_config('POSTGRES_USER', '', cast=str)
POSTGRES_PASSWORD = decouple_config('POSTGRES_PASSWORD', '', cast=str)

# HTML Elements
COOKIES_BUTTON_XPATH = decouple_config('COOKIES_BUTTON_XPATH', '', cast=str)
SEARCH_RESULTS_XPATH = decouple_config('SEARCH_RESULTS_XPATH', '', cast=str)
JOB_PAGE_RESULTS_XPATH = decouple_config('JOB_PAGE_RESULTS_XPATH', '', cast=str)
SEARCH_LOAD_MORE_BUTTON_XPATH = decouple_config('SEARCH_LOAD_MORE_BUTTON_XPATH', '', cast=str)
JOB_LOAD_MORE_BUTTON_XPATH = decouple_config('JOB_LOAD_MORE_BUTTON_XPATH', '', cast=str)
AUSBILDUNG_DE_BASE_URL = decouple_config('AUSBILDUNG_DE_BASE_URL', '', cast=str)

# Divs
CONTACT_DIV_CLASS = decouple_config('CONTACT_DIV_CLASS', '', cast=str)
NAME_DIV_CLASS = decouple_config('NAME_DIV_CLASS', '', cast=str)
POSITION_DIV_CLASS = decouple_config('POSITION_DIV_CLASS', '', cast=str)
EMAIL_DIV_CLASS = decouple_config('EMAIL_DIV_CLASS', '', cast=str)
PHONE_DIV_CLASS = decouple_config('PHONE_DIV_CLASS', '', cast=str)
DESCRIPTION_DIV_CLASS = decouple_config('DESCRIPTION_DIV_CLASS', '', cast=str)

# Selenium
GOOGLE_CHROME_BIN = decouple_config('GOOGLE_CHROME_BIN', '', cast=str)
CHROMEDRIVER_PATH = decouple_config('CHROMEDRIVER_PATH', '', cast=str)
SCROLL_BOTTOM_SCRIPT = decouple_config('SCROLL_BOTTOM_SCRIPT', '', cast=str)

WAIT_TIME = decouple_config('WAIT_TIME', 10, cast=int)
HEROKU_ENV = decouple_config('HEROKU_ENV', False, cast=bool)
COMMAND_EXECUTOR = decouple_config('COMMAND_EXECUTOR', 'http://selenium:4444', cast=str)
TELEGRAM_BOT_TOKEN = decouple_config('TELEGRAM_BOT_TOKEN', '', cast=str)
REDIS_URL = decouple_config('REDIS_URL', 'redis://redis:6379/0', cast=str)


def get_chrome_options() -> ChromeOptions:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("disable_infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    return chrome_options


def get_chrome_service():
    return Service(executable_path=CHROMEDRIVER_PATH)


def get_webdriver() -> WebDriver:
    if HEROKU_ENV:
        driver = webdriver.Chrome(
            service=get_chrome_service(),
            options=get_chrome_options()
        )
    else:
        driver: WebDriver = webdriver.Remote(
            command_executor=COMMAND_EXECUTOR,
            options=webdriver.FirefoxOptions()
        )
    return driver


SEARCH_PAGE = 'https://www.ausbildung.de/suche/?form_main_search[rlon]=9.481544&form_main_search[rlat]=51.312801&form_main_search[video_application_on]=&form_main_search[show_integrated_degree_programs]=1&form_main_search[show_educational_trainings]=1&form_main_search[show_qualifications]=1&form_main_search[show_regular_apprenticeships]=1&form_main_search[show_inhouse_trainings]=1&form_main_search[show_educational_trainings_and_regular_apprenticeships]=1&form_main_search[show_training_programs]=1&form_main_search[radius]=269&form_main_search[min_radius]=0&form_main_search[profession_public_id]=&form_main_search[profession_topic_public_id]=&form_main_search[industry_public_id]=&form_main_search[expected_graduation]=&form_main_search[starts_no_earlier_than]=&form_main_search[sort_order]=relevance&form_main_search[breaker_tile]=true&form_main_search[what]=Abiturientenprogramm%20im%20Vertrieb%20&form_main_search[where]=23909%20Albsfelde&t_search_type=main&t_what=Abiturientenprogramm%20im%20Vertrieb%20&t_where=23909%20Albsfelde'
JOBS_PAGE = 'https://www.ausbildung.de/berufe/zerspanungsmechaniker/stellen/#tab-bar-anchor'
