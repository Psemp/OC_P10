from django.core.management.base import BaseCommand
from research.models import Category
import requests


class Command(BaseCommand):
    help = 'Scans OFF API and stores Categories into DB'

    def handle(self, *args, **options):
        category_url = 'https://fr-fr.openfoodfacts.org/categories.json'
        print("loading")
        r = requests.get(category_url)
        category_page = r.json()

        for category in category_page['tags']:

            if 500 < category['products'] < 5500 and '-and-' not in category['id'] and category['name'][2] != ':':
                c = Category(name=category['id'], translated_name=category['name'],
                             url=category['url'], amount=category['products'])
                c.save()
        print("done")
        return
