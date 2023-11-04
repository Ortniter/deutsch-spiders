from tasks import app

from workers import contoller as worker_controller


@app.task
def scrape(session_id):
    worker_controller.run_worker(session_id)
