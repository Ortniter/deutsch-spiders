from decouple import config as decouple_config
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver

# HTML Elements
COOKIES_BUTTON_XPATH = decouple_config('COOKIES_BUTTON_XPATH', '', cast=str)
SEARCH_RESULTS_XPATH = decouple_config('SEARCH_RESULTS_XPATH', '', cast=str)
LOAD_MORE_BUTTON_XPATH = decouple_config('LOAD_MORE_BUTTON_XPATH', '', cast=str)
AUSBILDUNG_DE_BASE_URL = decouple_config('AUSBILDUNG_DE_BASE_URL', '', cast=str)
SEARCH_PAGE = decouple_config('SEARCH_PAGE', '', cast=str)

# Divs
CONTACT_DIV_CLASS = decouple_config('CONTACT_DIV_CLASS', '', cast=str)
NAME_DIV_CLASS = decouple_config('NAME_DIV_CLASS', '', cast=str)
POSITION_DIV_CLASS = decouple_config('POSITION_DIV_CLASS', '', cast=str)
EMAIL_DIV_CLASS = decouple_config('EMAIL_DIV_CLASS', '', cast=str)
PHONE_DIV_CLASS = decouple_config('PHONE_DIV_CLASS', '', cast=str)

# Selenium
GOOGLE_CHROME_BIN = decouple_config('GOOGLE_CHROME_BIN', '', cast=str)
CHROMEDRIVER_PATH = decouple_config('CHROMEDRIVER_PATH', '', cast=str)
SCROLL_BOTTOM_SCRIPT = decouple_config('SCROLL_BOTTOM_SCRIPT', '', cast=str)

WAIT_TIME = decouple_config('WAIT_TIME', 10, cast=int)
HEROKU_ENV = decouple_config('HEROKU_ENV', False, cast=bool)
COMMAND_EXECUTOR = decouple_config('COMMAND_EXECUTOR', 'http://localhost:4444', cast=str)
DATABASE_URL = decouple_config('DATABASE_URL', 'sqlite:///./sql_app.db', cast=str)
TELEGRAM_BOT_TOKEN = decouple_config('TELEGRAM_BOT_TOKEN', '', cast=str)
REDIS_URL = decouple_config('REDIS_URL', 'redis://redis:6379/0', cast=str)


def get_chrome_options() -> ChromeOptions:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
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
