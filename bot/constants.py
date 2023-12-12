from enum import Enum


class Actions(Enum):
    LIST_SESSIONS = 'list_sessions'
    AUSBILDUNG_PAGE = 'ausbildung_page'
    LOAD_RECORDS = 'load_records'
    GET_SUMMARY = 'get_summary'
    BACK = 'back'


SCRAPERS_TO_PAGES = {
    'ausbildung': Actions.AUSBILDUNG_PAGE.value,
}
