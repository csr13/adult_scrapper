import logging

from django.conf import settings
from rest_framework.permissions import BasePermission


logger = logging.getLogger(__name__)


class HasInternalUsagePermission(BasePermission):
    allowed_internal_access_addresses = settings.ALLOWED_INTERNAL_ACCESS_ADDRESSES
    message = "For internal usage only."

    def has_permission(self, request, view):
        if request.META["REMOTE_ADDR"] not in self.allowed_internal_access_addresses:
            logger.info(
                "%s tried to access %s resources, access denied." % (
                    request.META["REMOTE_ADDR"],
                    request.path
                )
            )
            return False
        return True
