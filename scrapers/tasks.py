from tasks import app

from scrapers.workers import controller as worker_controller


@app.task
def scrape(session_id):
    worker_controller.run_worker(session_id)
