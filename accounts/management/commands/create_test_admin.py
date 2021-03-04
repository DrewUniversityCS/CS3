from django.core.management.base import BaseCommand

from accounts.models import BaseUser


class Command(BaseCommand):
    """
    This will create a simple admin user (for testing purposes).
    """

    def handle(self, *args, **options):
        self._create_test_admin()

    def _create_test_admin(self):
        BaseUser.objects.create_superuser('admin', 'admin@gmail.com', '123')
