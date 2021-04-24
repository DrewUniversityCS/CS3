"""
File Name: Load Fixtures
Purpose: Command for loading default database data.
Comments:
"""

from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Loads necessary fixtures
    """

    fixtures = ["base_schedule.json", "departments.json", "teacher.json"]

    def handle(self, *args, **options):
        self._load_data()

    def _load_data(self):
        for json_file in self.fixtures:
            management.call_command("loaddata", json_file)
