from django.core.management import BaseCommand
import os
import shutil

class Command(BaseCommand):
    """command for remove software directory and archives"""
    def handle(self, *args, **options):
        remove_migrations_dir()
        self.stdout.write('Successfully remove common migrations!!')


def remove_migrations_dir():
    """remove apps migrations"""
    p = os.path.dirname(__file__)
    p = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(p))))
    for s in os.listdir(p):
        migration_dir = os.path.abspath(os.path.join(p, s,'migrations'))
        if os.path.exists(migration_dir):
            shutil.rmtree(migration_dir)


if __name__ == "__main__":
    remove_migrations_dir()
