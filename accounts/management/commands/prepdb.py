from django.core import management


class Command(management.base.BaseCommand):
    """
    Runs a bunch of commands to get the database ready for development.
    """

    def handle(self, *args, **options):
        management.call_command("run_default_migrations")
        management.call_command("load_fixtures")
        management.call_command("create_test_admin")
