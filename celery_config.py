from celery_app import celery
from celery.schedules import crontab

celery.conf.beat_schedule = {
    "fetch-13f-hr-every-week": {
        "task": "api.fetch_13f.fetch_and_store_13f",
        "schedule": crontab(day_of_week="monday", hour=6, minute=0),
    },
    "clean-redis-cache-every-week": {
        "task": "tasks.clean_redis_cache",
        "schedule": crontab(day_of_week="sunday", hour=3, minute=0),
    },
    "check-30f-filings-every-week": {
        "task": "tasks.check_and_update_30f",
        "schedule": crontab(day_of_week="monday", hour=5, minute=0),
    },
}
celery.conf.beat_schedule.update(
    {
        "clean-celery-metadata-every-day": {
            "task": "tasks.clean_celery_metadata",
            "schedule": crontab(hour=3, minute=0),
        }
    }
)


celery.conf.timezone = "UTC"

celery.conf.update(result_expires=3600)
