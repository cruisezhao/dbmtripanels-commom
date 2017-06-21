# import sys
# import django
# import os
# base = "D:/dbm/gitlab_test/bbbbbtripanel/admin/admin/admin/"
# sys.path.append(base)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")
# import pymysql
# pymysql.install_as_MySQLdb()
# django.setup()

from django.core.management import BaseCommand
from common.apps.products.models import (Products, Plans, Screenshot,
                                         Video,ProductApps)

class Command(BaseCommand):
    """delete products"""
    def add_arguments(self, parser):
        parser.add_argument('name')

    def handle(self,*args, **options):
        product_name = options.get('name', None)
        info = ''
        info = delete_products(product_name)
        self.stdout.write(info)


def delete_products(name):
    """delete products"""
    try:
        product = Products.objects.get(product_name = name)
    except Products.DoesNotExist:
        print("the record does not exist!")
    try:
        info = product.delete()
        return str(info)
    except:
        return "delete product failed"

if __name__ == "__main__":
    # import sys
    # import django
    # base = "D:/dbm/gitlab_test/bbbbbtripanel/admin/admin/admin/"
    # sys.path.append(base)
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")
    # import pymysql
    # pymysql.install_as_MySQLdb()
    # django.setup()

    #test
    delete_products("ecwid")
