import logging
import re
import threading

import requests
from rest_framework.response import Response

from api.connectors import FeedConnector
from manager.models import Blog, BdsmlrCredentials


logger = logging.getLogger(__name__)


class BlogsMixin:
    def blog_exists(self, blog):
        try:
            if not blog.endswith('.bdsmlr.com'):
                return False, "Only bdsmlr blogs allowed."
            check = requests.get(blog)
            if check.status_code != 200:
                raise Exception(
                    "%s does not exist, pinged and obtained %s" % (
                        blog,
                        check.status_code
                    )
                )
            check = re.search(
                r'This blog doesn\'t exist\.',
                check.content.decode("utf-8")
            )
            if check is not None:
                raise Exception(
                    "%s does not exist, pinged and obtained %s" % (
                        blog,
                        "This blog doesn't exist"
                    )
                )
        except Exception as error:
            logger.exception(str(error))
            return False, "Unable to add %s: Reason: %s" % (
                blog,
                str(error)
            )
        return True, "%s exists" % blog



class FeedMixin:
    def get_env_stats(self):
        env_stats = FeedConnector.get_env_stats()
        if not env_stats[0]:
            return Response(
                data=dict(error='Unable to get stats'), 
                status=400
            )
        data = dict(data=env_stats[1])
        return Response(data=data, status=200)

    def trigger_upload(self):
        check = FeedConnector.trigger_upload()
        if not check[0]:
            return Response(
                data=dict(error='Unable to trigger upload'), 
                status=400
            )
        return Response(
            data=dict(message='feed migration in progress.'),
            status=200
        )

    def set_env_status(self, status):
        check = FeedConnector.set_env_status(status)
        if not check[0]:
            return Response(
                data=dict(error='Unable to set feed switch'), 
                status=400
            )
        return Response(
            data=dict(message='Env set %s' % status),
            status=200
        )

    def trigger_manual_run(self, blog_uid):
        blog = Blog.objects.filter(uid=blog_uid)
        if not blog.exists():
            return Response(
                data=dict(
                    message="Blog %s does not exist" % blog_uid
                )
            )
        daemon = threading.Thread(
            target=FeedConnector.trigger_manual_run, 
            args=(blog.first().uid,)
        )
        daemon.daemon = True
        daemon.start()
        return Response(
            data=dict(message="Scrape for blog %s has been scheduled." % blog_uid),
            status=200
        )
    
    def get_manager_feed_credentials(self):
        creds = BdsmlrCredentials.objects.filter(
            flagged=False
        )
        if creds.count() == 0:
            return Response(
                data=dict(
                    error="Add some credentials on the manager !"
                ),
                status=400
            )
        return Response(
            data=[
                dict(
                    email=x.email, 
                    password=x.password
                ) for x in creds
            ],
            status=200
        )


