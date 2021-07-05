from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    translated_name = models.CharField(max_length=200, unique=False)
    url = models.URLField()
    amount = models.IntegerField()

    def __str__(self):
        return self.name


class Product(models.Model):
    barcode = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, unique=False)
    brand = models.CharField(max_length=200, unique=False)
    url = models.URLField(unique=True)
    picture_url = models.URLField(unique=True)
    product_categories = models.ManyToManyField(Category, related_name='product_categories', blank=True)
    nutriscore = models.CharField(max_length=3)
    stores = models.CharField(max_length=1000, blank=True, unique=False)

    # NUTRIMENTS

    sugars = models.FloatField(blank=True, default=-1)
    fats = models.FloatField(blank=True, default=-1)
    proteins = models.FloatField(blank=True, default=-1)
    kcals = models.FloatField(blank=True, default=-1)
    salt = models.FloatField(blank=True, default=-1)

    def __str__(self):
        return self.name
