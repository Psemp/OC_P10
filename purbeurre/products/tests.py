from django.test import TestCase
from django.urls import reverse
from research.models import Product
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
# Create your tests here.


class CompareTestCase(TestCase):
    def setUp(self):

        p1 = Product(barcode=1111111111111, name='p1', url='https://p1.org/',
                     brand='b1', picture_url='https://p1p.org/', nutriscore='e', stores='s1')
        p1.save()

        self.product = Product.objects.get(name='p1')

    def test_detail_page_200(self):
        barcode = self.product.barcode
        response = self.client.get(reverse('detail', args=(barcode,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_404(self):
        barcode = self.product.barcode + 1
        response = self.client.get(reverse('detail', args=(barcode + 1,)))
        self.assertEqual(response.status_code, 404)


class SeleniumTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.credentials = {
            'username': 'user_seleniumtest',
            'email': 'email@mail.com',
            'password': 'Password1'}
        User.objects.create_user(**self.credentials)

        picurl = 'https://3.bp.blogspot.com/-y464W7jp4Ss/UZi4oEMBO5I/AAAAAAAAAKE/_r96bf09wR4/s1600/cute+fish1.png'
        prod = Product(barcode=9999999999999, name='prod', url='https://prod.org/',
                       brand='brand', picture_url=picurl, nutriscore='e', stores='s1')
        prod.save()

    def test_fav_add(self):

        # Starting by logging setUp user
        self.selenium.get(self.live_server_url + '/login')
        time.sleep(1)
        username = self.selenium.find_element_by_id('id_username')
        password = self.selenium.find_element_by_id('id_password')
        submit = self.selenium.find_element_by_id('submit_button')
        username.send_keys('user_seleniumtest')
        password.send_keys('Password1')
        submit.send_keys(Keys.RETURN)
        time.sleep(1)
        self.selenium.implicitly_wait(10)

        # Then navigating to URL of setUp product
        self.selenium.get(self.live_server_url + '/detail/9999999999999')
        time.sleep(1)

        # Adding product to favorites then checking if it worked
        fav_add = self.selenium.find_element_by_id("fav_add_btn")
        fav_add.click()
        time.sleep(1)
        # The line below should not return an error except if the product was not
        # in user favorites
        self.selenium.find_element_by_id("faved_already")
