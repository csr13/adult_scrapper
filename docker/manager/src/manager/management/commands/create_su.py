from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    help = "Creates the default user"

    user = {
        "email" : "admin@manager.com",
        "username" : "admin",
        "password" : "Manager!@#"
    }

    def add_arguments(self, parser):
        return None

    def handle(self, *args, **options):
        if User.objects.filter(email=self.user["email"]).exists():
            self.stdout.write(self.style.SUCCESS("Super user Details:"))
            for k, v in self.user.items():
                self.stdout.write(self.style.ERROR("{} => {}".format(k, v)))
                exit(0)

        User.objects.create_superuser(**self.user)
        self.stdout.write(self.style.SUCCESS("Super user Details:"))
        for k, v in self.user.items():
            self.stdout.write(self.style.ERROR("{} => {}".format(k, v)))
        exit(0)
