import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from manager.models import Feed, Category


class Command(BaseCommand):
    
    help = "Seeds database table's with initial data."

    def add_arguments(self, parser):
        return None


    def feed_migration(self):
        main_feed = {
            "name" : "Main Feed",
            "url" : "http://feed:8888"
        }
        if not Feed.objects.filter(
            slug=slugify(
                main_feed["name"]
            )
        ).exists():
            Feed.objects.create(**main_feed)
            self.stdout.write(self.style.SUCCESS(
                "Main feed %s created" % main_feed
            ))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Feed: %s already exists." % main_feed["name"]
                )
            )
        return True

    
    def migrate_inital_categories(self):
        if not os.path.exists(
            os.path.join(settings.BASE_DIR, 'data', 'categories.txt')
        ):
            self.stdout.write(
                self.style.ERROR(
                    "No categories.txt file on data dir to load from."
                )
            )
        # load the categories.
        categories = []
        with open(
            os.path.join(
                settings.BASE_DIR, 
                'data', 
                'categories.txt'
            ), 
            "r"
        ) as ts:
            for each in ts.readlines():
                name = each.strip("\n").capitalize()
                if not Category.objects.filter(name=name).exists():
                    categories.append(
                        Category(
                            name=name,
                            slug=slugify(name)
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS("Loading category => %s" % each.strip("\n"))
                    )

                else:
                    self.stdout.write(
                        self.style.SUCCESS("Category Exists => %s" % each.strip("\n"))
                    )
        # Bulk create the categories.
        Category.objects.bulk_create(categories)
        self.stdout.write(
            self.style.SUCCESS(
                "Created %s categories for blogs." % len(categories)
            )
        )

    def handle(self, *args, **options):
        self.feed_migration()
        self.migrate_inital_categories()
