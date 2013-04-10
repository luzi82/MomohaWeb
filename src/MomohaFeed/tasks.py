from celery.schedules import crontab
from celery.task import periodic_task
from django.core.cache import cache

import logging
import MomohaFeed

logger = logging.getLogger(__name__)

@periodic_task(run_every=crontab())
def periodic_update_feed_pool():
    
    LOCK_ID = "periodic_update_feed_pool"
    LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes
    UPDATE_TIMEOUT = 15*60*1000
    
    acquire_lock = lambda: cache.add(LOCK_ID, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(LOCK_ID)

    if acquire_lock():
        try:
            logger.info("update_feed_pool");
            MomohaFeed.update_feed_pool(UPDATE_TIMEOUT)
        finally:
            release_lock()
