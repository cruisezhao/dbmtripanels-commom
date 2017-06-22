from django.core.management import BaseCommand
import os
import shutil
import sys
# import django
# base = "D:/dbm/gitlab_test/bbbbbtripanel/admin/admin/admin/"
# sys.path.append(base)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")
# import pymysql
# pymysql.install_as_MySQLdb()
# django.setup()
from django.conf import settings



class Command(BaseCommand):
    """command for remove software directory and archives"""
    def add_arguments(self,parser):
        parser.add_argument('name')

    def handle(self, *args, **options):
        product_name = options.get('name',None)
        remove_directory(product_name)
        self.stdout.write('Successfully remove  "%s"' % product_name)


def remove_directory(name):
    """delete directory and archive"""
    arch_path = os.path.join(settings.SOFTWARE_ARCH, name + ".zip")
    dir_path = os.path.join(settings.SOFTWARE_DIR, name)
    if os.path.exists(arch_path):
        os.remove(arch_path)
        print("delete acrchives successully!")
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print("delete directory successfully!")
    print("done!")


if __name__ == "__main__":
    remove_directory("ecwid")
