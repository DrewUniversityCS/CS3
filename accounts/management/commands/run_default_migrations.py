"""
File Name: Default Migrations
Purpose: Custom command for making a bunch of migrations and running them.
Comments:
"""

from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    This will make migrations for all the apps and then runs migrate.
    """

    apps_to_migrate = ['accounts', 'database', 'dataingest']

    def handle(self, *args, **options):
        self._load_data()

    def _load_data(self):
        for app in self.apps_to_migrate:
            management.call_command('makemigrations', app)

        management.call_command('migrate')
