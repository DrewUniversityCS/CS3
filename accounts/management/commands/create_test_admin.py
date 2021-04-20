from django.core.management.base import BaseCommand

from accounts.models import BaseUser


class Command(BaseCommand):
    """
    This will create a simple admin user (for testing purposes).
    """

    def handle(self, *args, **options):
        self._create_test_admin()

    def _create_test_admin(self):
        if not BaseUser.objects.get(email='admin@gmail.com'):
            BaseUser.objects.create_superuser('admin', 'admin@gmail.com', '123')
            BaseUser.objects.filter(is_superuser=True).update(
                first_name='Super', last_name='User'
            )
