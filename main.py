from fastapi import FastAPI
from sqladmin import Admin

from db import engine
from scrapers.admin import model_views as scrapers_admin_views

app = FastAPI()
admin = Admin(app, engine)
admin.add_view(*scrapers_admin_views)


@app.get("/")
async def root():
    return {"message": "Hello World"}
