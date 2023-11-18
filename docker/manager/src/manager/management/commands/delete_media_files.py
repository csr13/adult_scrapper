"""
This is a cleanup script that should run as cron until, post crud signals
are added to DirtyImage model.
"""

import os

from django.core.management.base import BaseCommand
from django.conf import settings

from manager.models import DirtyImage


class Command(BaseCommand):
    
    help = "Deletes all media files, nuclear."
    
    def add_arguments(self, parser):
        return None

    def handle(self, *args, **options):
        dirty_images = settings.MEDIA_ROOT / 'dirty_images'
        if os.path.exists(dirty_images):
            for image in os.listdir(dirty_images):
                image_name = image.split(".")[0]
                if DirtyImage.objects.filter(name=image_name).exists():
                    self.stdout.write(
                        self.style.SUCCESS(
                            "%s exists, skipping deletion" %image_name
                        )
                    )
                    continue
                self.stdout.write(self.style.SUCCESS("Deleting %s." % image))
                os.unlink(
                    os.path.join(
                        dirty_images, 
                        image
                    )
                )
                self.stdout.write(self.style.SUCCESS("Image %s deleted." % image))
        exit(0)
