from django.core.management.base import BaseCommand
from django.db import DataError
from research.models import Category, Product
import requests


class Command(BaseCommand):

    help = 'Searches OFF API and saves products into DB by category'

    def handle(self, *args, **options):
        """Scans and saves relevant products per categories in DB"""
        barcode_list = []
        cat_obj_list = Category.objects.all()

        def sections_in_prod(prod):
            """returns true if relevant sections are in the product description"""
            if 'product_name' in prod and 'categories_hierarchy' in prod and 'brands' in prod and 'nutriscore_grade' in prod and 'stores' in prod and 'image_front_url' in prod:
                return True
            else:
                return False

        def bc_test(barcode):
            if len(barcode) == 13:
                return True
            elif len(barcode) < 13:
                return False
            else:
                return False

        def length_management(string):
            return len(string) < 199

        print('This will take a while')
        for category in cat_obj_list:
            page_api = 1

            while page_api < 2:  # (category.amount/20):  # +/- 20 products per page
                # We limit the number of pages searched otherwise it will be still running by the next ice age
                formatted_url = category.url + f'/{page_api}.json'
                r = requests.get(formatted_url)
                products_page = r.json()
                print('loading ...')

                for product in products_page['products']:
                    if product['_id'] in barcode_list:
                        try:
                            p = Product.objects.get(barcode=product['_id'])
                            p.product_categories.add(category.pk)
                            p.save()
                        except:
                            print("Unknown error, Skipping product")
                    elif product['_id'] not in barcode_list and sections_in_prod(product) and bc_test(product['_id']) and length_management(product['product_name']):
                        try:
                            p = Product(barcode=product['_id'], name=product['product_name'], url=product['url'],
                                        brand=product['brands'], picture_url=product['image_front_url'],
                                        nutriscore=product['nutriscore_grade'], stores=product['stores'])

                            if 'sugars_100g' in product['nutriments']:
                                p.sugars = product['nutriments']['sugars_100g']
                            if 'salt_100g' in product['nutriments']:
                                p.salt = product['nutriments']['salt_100g']
                            if 'energy-kcal_100g' in product['nutriments']:
                                p.kcals = product['nutriments']['energy-kcal_100g']
                            if 'proteins_100g' in product['nutriments']:
                                p.proteins = product['nutriments']['proteins_100g']
                            if 'fat_100g' in product['nutriments']:
                                p.fats = product['nutriments']['fat_100g']

                            barcode_list.append(product['_id'])
                            p.save()
                            p.product_categories.add(category.pk)
                            p.save()
                        except ValueError:
                            print("Data incompatible, skipping -- Value Error")
                        except DataError:
                            print("Data incompatible, skipping -- Data Error, name too long")
                    page_api += 1
        print('done')
        return
