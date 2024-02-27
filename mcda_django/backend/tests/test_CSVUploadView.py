from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

class CSVUploadView_TestCase(APITestCase):

    def test_non_csv(self):
        url = reverse('backend:api_method', kwargs={'method_name': 'topsis'})
        response = self.client.post(url, content_type='application/json',data='not a csv')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Wrong content type')

    @patch('backend.views.CSVDataProcessor')
    def test_post_csv_with_error(self, mock_processor):
        mock_processor.side_effect = ValueError('error')
        url = reverse('backend:api_method', kwargs={'method_name': 'topsis'})
        response = self.client.post(url, content_type='text/csv', data='a,b,c')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'error')

    @patch('backend.views.CSVDataProcessor')
    def test_post_processor_error(self, mock_processor):
        mock_processor.side_effect = Exception('error')
        url = reverse('backend:api_method', kwargs={'method_name': 'topsis'})
        response = self.client.post(url, content_type='text/csv', data='a,b,c')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Error processing data')

    @patch('backend.views.CSVDataProcessor')
    def test_post_valid_csv(self,mock_processor):
        mock_processor.return_value.preferences = [1,2,3]
        mock_processor.return_value.ranking = [1,2,3]
        mock_processor.return_value.alts_number = 3
        url = reverse('backend:api_method', kwargs={'method_name': 'topsis'})
        response = self.client.post(url, content_type='text/csv', data='a,b,c')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'CSV data uploaded')
        self.assertEqual(response.data['preferences'], [1,2,3])
        self.assertEqual(response.data['ranks'], [1,2,3])
        self.assertEqual(response.data['alts_number'], 3)

    