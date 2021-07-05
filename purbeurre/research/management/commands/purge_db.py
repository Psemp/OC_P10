from research.models import Product, Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'deletes all data from db'

    def handle(self, *args, **options):
        print('purging database ...')
        catset = Category.objects.all()
        for cat in catset:
            cat.delete()
        prodset = Product.objects.all()

        for prod in prodset:
            prod.delete()
        print('done')
        return
