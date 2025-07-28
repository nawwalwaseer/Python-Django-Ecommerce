from django.test import TestCase
from django.test import Client

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sayhello_view(self):
        response = self.client.get('/playground/sayhello/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nawwal Aftab Waseer")

    def test_contact_view_get(self):
        response = self.client.get('/playground/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gender")  

    def test_contact_view_post_valid(self):
        response = self.client.post('/playground/contact/', {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hello!',
            'gender': 'male',
            'country': 'USA',
            'address': '123 Main St'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thankyou.html')
        self.assertContains(response, "John Doe")

    def test_contact_view_post_invalid(self):
        response = self.client.post('/playground/contact/', {
            'name': '',
            'email': 'invalid',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
