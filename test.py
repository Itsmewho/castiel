from connection.connect_redis import get_redis_client
from tasks import clean_redis_cache, check_and_update_30f, clean_celery_metadata

# Test Redis Cache Cleanup
clean_redis_cache()

# Test MongoDB Update
check_and_update_30f()

# clean data
clean_celery_metadata()

redis_client = get_redis_client()
print(redis_client.keys("*"))
