import logging
import threading

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import View

from api.connectors import FeedConnector
from manager.models import Blog


logger = logging.getLogger(__name__)


class ManualSingleScrapeAdminAction(
    FeedConnector, 
    LoginRequiredMixin, 
    View
):
    def get(self, request, *args, **kwargs):
        # make an admin view that checks this and use it.
        if not request.user.is_superuser or not request.user.is_staff:
            return HttpResponseRedirect(
                reverse(
                    "admin:login"
                )
            )
        uid = kwargs["uid"]
        if not Blog.objects.filter(uid=uid).exists():
            messages.error(
                request, 
                "Invalid blog :> %s " % uid
            )
            return HttpResponseRedirect(
                reverse(
                    "admin:%s_%s_changelist" % (
                        "manager", 
                        "blog"
                    )
                )
            )
        daemon = threading.Thread(
            target=self.trigger_manual_run,
            args=(uid,)
        )
        daemon.daemon = True
        daemon.start()
        messages.info(
            request, 
            "Scrape instruction sent to feed for blog %s" % uid
        )
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_changelist" % (
                    "manager",
                    "blog"
                )
            )
        )
