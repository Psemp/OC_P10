from django.test import TestCase
from django.urls import reverse
from .script.compare import compare_products, get_product_categories, get_similar_prod

from .models import Category, Product
# Create your tests here.


class IndexPageTestCase(TestCase):

    # test that index returns a 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):

    # test that legal returns a 200
    def test_legal_page(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)


class CompareTestCase(TestCase):
    def setUp(self):

        Category.objects.create(name="c1", translated_name='c1', url='https://seashepherd.org/', amount=2)
        c = Category.objects.get(name='c1')
        self.c = c

        p1 = Product(barcode=1111111111111, name='p1', url='https://p1.org/',
                     brand='b1', picture_url='https://p1p.org/', nutriscore='e', stores='s1')

        p1.product_categories.add(c.pk)
        self.p1 = p1
        p1.save()

        p2 = Product(barcode=2222222222222, name='p2', url='https://p2.org/',
                     brand='b2', picture_url='https://p2p.org/', nutriscore='a', stores='s2')

        p2.product_categories.add(c.pk)
        self.p2 = p2
        p2.save()

        self.product = Product.objects.get(name='p1')

    def test_get_product_categories(self):
        """Tests that first cat in queryset recovered by script is c"""
        self.assertIn(self.c, get_product_categories(self.p1))

    def test_get_similar_prod(self):
        """Tests that p2 in similar product (as p1)"""
        test_cat_set = [self.c]
        self.assertIn(self.p2, get_similar_prod(test_cat_set))

    def test_compare_products(self):
        """Tests p2 in healthierlist of p1"""
        test_prodlist = [self.p2]
        self.assertIn(self.p2, compare_products(self.p1, test_prodlist))

    def test_comparison_page_200(self):
        barcode = self.product.barcode
        response = self.client.get(reverse('comparison', args=(barcode,)))
        self.assertEqual(response.status_code, 200)

    def test_comparison_page_404(self):
        barcode = self.product.barcode + 1
        response = self.client.get(reverse('comparison', args=(barcode,)))
        self.assertEqual(response.status_code, 404)
