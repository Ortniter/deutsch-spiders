from decouple import config as decouple_config
from selenium.webdriver import ChromeOptions

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


def get_chrome_options() -> ChromeOptions:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    return chrome_options
