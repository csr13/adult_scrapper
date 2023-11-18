import logging

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.connectors import FeedConnector
from api.mixins import FeedMixin
from api.permissions.access_permissions import HasInternalUsagePermission

logger = logging.getLogger(__name__)


class LoadManagerCredentials(FeedMixin, APIView):
    authentication_classes = settings.AUTHENTICATION_CLASSES
    permission_classes = settings.PERMISSION_CLASSES + [HasInternalUsagePermission]
    def get(self, request, *args, **kwargs):
        return self.get_manager_feed_credentials()


class FeedStats(FeedMixin, APIView):
    authentication_classes = settings.AUTHENTICATION_CLASSES
    permission_classes = settings.PERMISSION_CLASSES + [HasInternalUsagePermission]
    def get(self, request, *args, **kwargs):
        return self.get_env_stats()


class EnvSwitch(FeedMixin, APIView):
    authentication_classes = settings.AUTHENTICATION_CLASSES
    permission_classes = settings.PERMISSION_CLASSES + [HasInternalUsagePermission]
    def post(self, request, *args, **kwargs):
        status = kwargs["status"]
        return self.set_env_status(status)
