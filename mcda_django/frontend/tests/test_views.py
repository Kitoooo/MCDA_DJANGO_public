from django.test import TestCase
from django.urls import reverse

class FrontendViews_TestsCase(TestCase):

    def test_index_view(self):
        url = reverse('frontend:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('available_methods', response.context)

    def test_valid_method_view(self):
        url = reverse('frontend:method', kwargs={'method_name': 'topsis'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'method.html')
        self.assertIn('method_name', response.context)
        self.assertIn('available_methods', response.context)

    def test_invalid_method_view(self):
        url = reverse('frontend:method', kwargs={'method_name': 'invalid_method'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('frontend:index'))
