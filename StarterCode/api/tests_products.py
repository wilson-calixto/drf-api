import json
from rest_framework.test import APITestCase

from .models import Order,User,Product
from django.urls import reverse
from rest_framework import status
# Createyour tests here.


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        self.product = Product.objects.create(
            name='Test Product',
            description='test description',
            price=9.99,
            stock=10
        )
        self.url = reverse('product-detail', kwargs={'product_id':self.product.pk})

    def test_get_products(self):
        response = self.client.get(self.url) 
        print('json.loads(response.content)',json.loads(response.content))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),{'name': 'Test Product', 'description': 'test description', 'price': '9.99', 'stock': 10})
        
    def test_unauthorized_update_products(self):
        data={"name":"updated product"}
        response = self.client.put(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_products(self):        
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_only_admins_can_delete_products(self):
        self.client.login(username='user', password='userpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_only_admins_can_delete_products(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
                