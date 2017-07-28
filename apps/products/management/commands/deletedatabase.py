from django.core.management import BaseCommand
import os
import shutil

class Command(BaseCommand):
    """command for remove software directory and archives"""
    def handle(self, *args, **options):
        delete_database()
        create
        self.stdout.write('Successfully remove common migrations!!')
