from django.test import TestCase
from django.test.client import Client
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import auth
import datetime
import re

from djaffar.models import Activity


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_log_get(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.get('/djaffar/logs/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Activity.objects.count(), 0)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )

    def test_log_post_blank(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post('/djaffar/logs/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Activity.objects.count(), 0)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )

    def test_log_post_date(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Activity.objects.count(), 0)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )

    def test_log_post_date_referer(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
            },
            HTTP_REFERER='/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )
        self.assertEqual(Activity.objects.count(), 1)
        activity_obj = Activity.objects.first()
        self.assertFalse(activity_obj.user)
        self.assertEqual(
            activity_obj.session.session_key,
            self.client.session.session_key,
        )
        self.assertTrue(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            activity_obj.ip_address,
        ))
        self.assertTrue(activity_obj.date)
        self.assertEqual(
            activity_obj.path,
            '/',
        )
        self.assertFalse(activity_obj.referer)

    def test_log_post_date_path(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
                'path': '/',
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )
        self.assertEqual(Activity.objects.count(), 1)
        activity_obj = Activity.objects.first()
        self.assertFalse(activity_obj.user)
        self.assertEqual(
            activity_obj.session.session_key,
            self.client.session.session_key,
        )
        self.assertTrue(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            activity_obj.ip_address,
        ))
        self.assertTrue(activity_obj.date)
        self.assertEqual(
            activity_obj.path,
            '/',
        )
        self.assertFalse(activity_obj.referer)

    def test_log_post_date_referer_path(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
                'path': 'specified/path/',
            },
            HTTP_REFERER='/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )
        self.assertEqual(Activity.objects.count(), 1)
        activity_obj = Activity.objects.first()
        self.assertFalse(activity_obj.user)
        self.assertEqual(
            activity_obj.session.session_key,
            self.client.session.session_key,
        )
        self.assertTrue(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            activity_obj.ip_address,
        ))
        self.assertTrue(activity_obj.date)
        self.assertEqual(
            activity_obj.path,
            'specified/path/',
        )
        self.assertFalse(activity_obj.referer)

    def test_log_post_session_blank(self):
        client_old_session_key = self.client.session.session_key
        self.client.session.delete()
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
            },
            HTTP_REFERER='/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(
            self.client.session.session_key,
            client_old_session_key,
        )
        self.assertEqual(Activity.objects.count(), 1)
        activity_obj = Activity.objects.first()
        self.assertFalse(activity_obj.user)
        self.assertEqual(
            activity_obj.session.session_key,
            self.client.session.session_key,
        )
        self.assertTrue(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            activity_obj.ip_address,
        ))
        self.assertTrue(activity_obj.date)
        self.assertEqual(
            activity_obj.path,
            '/',
        )
        self.assertFalse(activity_obj.referer)

    def test_log_post_authenticated_user(self):
        user = auth.models.User.objects.create_user(
            username='jeff',
            password='koons',
        )
        self.client.login(
            username='jeff',
            password='koons',
        )
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
            },
            HTTP_REFERER='/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            client_session_key_before_post,
            self.client.session.session_key,
        )
        self.assertEqual(Activity.objects.count(), 1)
        activity_obj = Activity.objects.first()
        self.assertTrue(activity_obj.user)
        self.assertEqual(
            activity_obj.user.username,
            user.username,
        )
        self.assertEqual(
            activity_obj.session.session_key,
            self.client.session.session_key,
        )
        self.assertTrue(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            activity_obj.ip_address,
        ))
        self.assertTrue(activity_obj.date)
        self.assertEqual(
            activity_obj.path,
            '/',
        )
        self.assertFalse(activity_obj.referer)

    def test_log_post_referer_header_and_parameter(self):
        client_session_key_before_post = self.client.session.session_key
        response = self.client.post(
            '/djaffar/logs/',
            {
                'date': datetime.datetime.utcnow().isoformat(),
                'referer': 'https://google.com',
            },
            HTTP_REFERER='/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            self.client.session.session_key,
            client_session_key_before_post,
        )
        self.assertEqual(Activity.objects.count(), 1)
        activity_obj = Activity.objects.first()
        self.assertFalse(activity_obj.user)
        self.assertEqual(
            activity_obj.session.session_key,
            self.client.session.session_key,
        )
        self.assertTrue(re.match(
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            activity_obj.ip_address,
        ))
        self.assertTrue(activity_obj.date)
        self.assertEqual(
            activity_obj.path,
            '/',
        )
        self.assertTrue(
            activity_obj.referer,
            'https://google.com',
        )
