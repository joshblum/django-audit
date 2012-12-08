from django.utils import unittest
from django.test import Client

class TestGet(unittest.TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='fred', password='secret')

    def test_details(self):
        response = self.client.get('/login/', {'name': 'fred', 'passwd': 'secret'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['customers']), 5)

class TestPost(unittest.TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_details(self):
        response = self.client.post('/login/', {'name': 'fred', 'passwd': 'secret'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['customers']), 5)