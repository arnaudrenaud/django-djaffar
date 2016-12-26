from django.test import TestCase
from django.test.client import Client


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_log_request(self):
        response = self.client.get('/djaffar/logs/')
        self.failUnlessEqual(response.status_code, 405)

    def test_empty_post_log_request(self):
        response = self.client.post('/djaffar/logs/')
        self.failUnlessEqual(response.status_code, 400)
