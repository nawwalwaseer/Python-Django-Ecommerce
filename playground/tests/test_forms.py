from django.test import TestCase
from playground.forms import ContactForm

class ContactFormTest(TestCase):
    def test_valid_data(self):
        form = ContactForm(data={
            'name': 'Alice',
            'email': 'alice@example.com',
            'message': 'Hello!',
            'gender': 'female', 
            'country': 'Wonderland',
            'address': '123 Street'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = ContactForm(data={
            'name': '',
            'email': 'not-an-email'
        })
        self.assertFalse(form.is_valid())   
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
