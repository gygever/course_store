from django.test import TestCase
from django.contrib.auth.models import User


class SignUpTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='testuser1', email='test.email.1@gmail.com', password='1q2w3e4r5t6y7u)')

    def tearDown(self):
        pass

    def test_sign_up_loads_properly(self):
        response = self.client.get('/sign_up/')
        self.assertEqual(response.status_code, 200)

    def test_correct_data(self):
        response = self.client.post('/sign_up/', {'username': 'testuser', 'email': 'test.email@gmail.com', 'password1': '1q2w3e4r5t6y7u)', 'password2': '1q2w3e4r5t6y7u)'}, follow=True)
        user = User.objects.filter(username='testuser').all()
        self.assertTrue(user[0])
        self.assertRedirects(response, '/')

    def test_short_username(self):
        response = self.client.post('/sign_up/', {'username': 'tes', 'email': 'test.email@gmail.com', 'password1': '1q2w3e4r5t6y7u)', 'password2': '1q2w3e4r5t6y7u)'}, follow=True)
        user = User.objects.filter(username='tes').all()
        self.assertFalse(user)
        self.assertEqual(response.status_code, 200)

    def test_long_username(self):
        response = self.client.post('/sign_up/', {'username': 't' * 200, 'email': 'test.email@gmail.com', 'password1': '1q2w3e4r5t6y7u)', 'password2': '1q2w3e4r5t6y7u)'}, follow=True)
        user = User.objects.filter(username='t' * 200).all()
        self.assertFalse(user)
        self.assertEqual(response.status_code, 200)

    def test_existing_email(self):
        response = self.client.post('/sign_up/', {'username': 'testuser2', 'email': 'test.email.1@gmail.com', 'password1': '1q2w3e4r5t6y7u)', 'password2': '1q2w3e4r5t6y7u)'}, follow=True)
        self.assertTrue(b'Email Already Exist' in response.content)
        self.assertEqual(response.status_code, 200)

    def test_logged_try_open(self):
        login = self.client.login(username='testuser1', password='1q2w3e4r5t6y7u)')
        response = self.client.get('/sign_up/', follow=True)
        self.assertRedirects(response, '/')


class LogInTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser1', email='test.email.1@gmail.com', password='1q2w3e4r5t6y7u)')

    def tearDown(self):
        pass

    def test_correct_data(self):
        response = self.client.post('/log_in/', {'username': 'testuser1', 'password': '1q2w3e4r5t6y7u)'}, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, '/')

    def test_logged_try_open(self):
        login = self.client.login(username='testuser1', password='1q2w3e4r5t6y7u)')
        response = self.client.get('/log_in/', follow=True)
        self.assertRedirects(response, '/')

    def test_short_username(self):
        response = self.client.post('/log_in/', {'username': 'test', 'password': '1q2w3e4r5t6y7u)'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_long_username(self):
        response = self.client.post('/log_in/', {'username': 't' * 200, 'password': '1q2w3e4r5t6y7u)'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_username(self):
        response = self.client.post('/log_in/', {'username': 'invalid', 'password': '1q2w3e4r5t6y7u)'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_password(self):
        response = self.client.post('/log_in/', {'username': 'testuser1', 'password': 'invalid'}, follow=True)
        self.assertEqual(response.status_code, 200)
