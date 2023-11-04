import celery

import config

app = celery.Celery('tasks')
app.conf.update(BROKER_URL=config.REDIS_URL, CELERY_RESULT_BACKEND=config.REDIS_URL)
