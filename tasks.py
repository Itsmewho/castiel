from datetime import datetime
from celery_app import celery, logger
from utils.helpers import red, green, reset
from db.db_operations import insert_document
from connection.connect_redis import get_redis_client


@celery.task
def check_and_update_30f():
    try:
        new_filing = {
            "company_name": "Example Hedge Fund",
            "filing_date": datetime.now(
                datetime.timezone.utc
            ),  # Use UTC for consistency
            "top_holdings": [{"stock": "AAPL", "price": 150, "growth": 5.2}],
        }
        insert_document("renaissance", new_filing)
        logger.info(green + "Weekly 30F filings updated successfully." + reset)
    except Exception as e:
        logger.error(red + f"Error updating 30F filings: {e}" + reset)


@celery.task
def clean_redis_cache():
    redis_client = get_redis_client()
    try:
        keys = redis_client.keys("*")
        for key in keys:
            if key.startswith("celery-task-meta-") or key.startswith("_kombu.binding."):
                continue  # Skip Celery-related keys
            ttl = redis_client.ttl(key)
            if ttl == -1:  # Keys with no expiration
                redis_client.delete(key)
        logger.info(green + "Redis cache cleaned successfully." + reset)
    except Exception as e:
        logger.error(red + f"Error during Redis cache cleanup: {e}" + reset)


@celery.task
def clean_celery_metadata():
    redis_client = get_redis_client()
    try:
        # Clean Celery metadata keys
        keys = redis_client.keys("celery-task-meta-*")
        for key in keys:
            redis_client.delete(key)

        # Clean Kombu bindings
        keys = redis_client.keys("_kombu.binding.*")
        for key in keys:
            redis_client.delete(key)

        logger.info(green + f"Cleared Celery task metadata and routing keys.{reset}")
    except Exception as e:
        logger.error(red + f"Failed to clear Celery metadata keys: {e}{reset}")
