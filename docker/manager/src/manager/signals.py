import logging

from django.db.models.signals import post_delete
from django.dispatch import receiver


from manager.models import DirtyImage
from manager.utils import delete_object_from_media


logger = logging.getLogger(__name__)


@receiver(post_delete, sender=DirtyImage)
def delete_image_from_media(sender, instance, **kwargs):
    logger.info("[SIGNAL] Deleting %s from media" % instance.name)
    delete_object_from_media(instance)

