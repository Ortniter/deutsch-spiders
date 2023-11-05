from sqladmin import ModelView

from scrapers.models import ScrapingSession


class ScrapingSessionAdmin(ModelView, model=ScrapingSession):
    form_columns = [
        ScrapingSession.url,
        ScrapingSession.scraper,
        ScrapingSession.file,
    ]
    column_list = [
        ScrapingSession.id,
        ScrapingSession.created_at,
        ScrapingSession.status,
        ScrapingSession.scraper,
    ]
    column_details_exclude_list = [ScrapingSession.id, ScrapingSession.records]


model_views = [ScrapingSessionAdmin]
