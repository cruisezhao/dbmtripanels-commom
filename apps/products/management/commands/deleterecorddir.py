from .deleteproductrecord import delete_products
from .removeproducts import remove_directory
from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name')

    def handle(self,*args,**options):
        product_name = options.get('name', None)
        remove_directory(product_name)
        self.stdout.write("remove dir success!")
        info = delete_products(product_name)
        self.stdout.write("remove record success!")

