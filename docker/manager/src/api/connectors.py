import logging
import time

import requests
from django.conf import settings

from manager.models import Blog, ScrapeLog


logger = logging.getLogger(__name__)


class FeedConnector:

    @classmethod
    def update_env_blogs(cls, delay=0):
        time.sleep(delay)
        logger.info("[SIGNAL] Updating feed blogs after adding new blog")
        try:
            resp = requests.post(
                "%s/%s" % (
                    settings.FEED_URL,
                    "update-env-blogs"
                )
            )
            if resp.status_code != 200:
                raise Exception("Invalid response from feed") from None
        except Exception as error:
            logger.info(str(error))
            return False
        logger.info("[SIGNAL] Feed blogs updated from manager.")
        return True

    @classmethod
    def get_env_stats(cls):
        try:
            resp = requests.get(
                "%s/%s" % (
                    settings.FEED_URL, 
                    "env-stats"
                )
            )
            if resp.status_code != 200:
                raise Exception("Unable to get stats from feed") from None
        except Exception as error:
            logger.info(str(error))
            return False, None
        return True, resp.json()
    
    @classmethod
    def set_env_status(cls, status):
        try:
            resp = requests.post(
                "%s/%s" % (
                    settings.FEED_URL, 
                    "on-off"
                ), 
                data={
                    "status" : status
                }
            )
            if resp.status_code != 200:
                raise Exception("Unable to set status %s" % status) from None
        except Exception as error:
            logger.info(str(error))
            return False, None
        return True, resp.json()

    @classmethod
    def trigger_manual_run(cls, blog_uid):
        logger.info("Sending scrape for blog %s" % blog_uid)
        try:
            resp = requests.post(
                "%s/%s" % (
                    settings.FEED_URL, 
                    "manual-run/single/%s" % blog_uid
                ), 
            )
            if resp.status_code != 200:
                raise Exception(
                    "Feed returned %s for manual run" % resp.status_code
                ) from None
        except Exception as error:
            logger.info(str(error))
            ScrapeLog.cook_scrape(
                blog_uid, 
                {
                    "scrape_data" : {
                        "success"  : False,
                        'error' : str(error)
                    }
                }
            )
            return False, None
        ScrapeLog.cook_scrape(
            blog_uid, 
            resp.json()
        )
        return True, resp.json()

    @classmethod
    def trigger_bulk_scrape(cls, uids):
        try:
            resp = requests.post(
                "%s/%s" % (
                    settings.FEED_URL,
                    "/bulk-runs",
                ),
                data={"uids" : uids}
            )
            if resp.status_code != 200:
                raise Exception("Error builkscraping") from None
            ScrapeLog.cook_multiple_scrapes(
                uids,
                resp.json()
            )
        except Exception as error:
            logger.info(str(error))
            ScrapeLog.cook_multiple_scrapes(
                uids,
                {
                    'scrape_data' : {
                        'success' : False,
                        'error' : str(error)
                    }
                }
            )
            return False, None
        return True, resp.json()


