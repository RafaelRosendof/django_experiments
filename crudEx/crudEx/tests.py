from rest_framework.test import APITestCase
from rest_framework import status
from .models.client import Client
from django.contrib.auth.models import User

class ClientAPITestCase(APITestCase):

    def setUp(self):
        url = '/api/clients/'
        url_token = '/api/token/'

        self.user = User.objects.create_user(username='rafael', password='rafinha19')

        body_token = {
            "username": "rafael",
            "password": "rafinha19"
        }

        token_response = self.client.post(url_token , body_token , format='json')


        #print("Token debug:" , token_response)
        #print("Token response:", token_response.data)

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.token = token_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        print("Setup complete. Token obtained.")
    
        data = {
            "name": "Test Client Inc.",
            "email": "test@innovatebr.com",
            "phones": [{"phone_number": "123456789"}],
            "addresses": [{"address_line": "123 Test St", "city": "Testville", "postal_code": "12345"}]
        }

        
        response = self.client.post(url , data , format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().name, 'Test Client Inc.')


class ClientAddTest(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='rafael', password='rafinha19')

        cls.client_url = '/api/clients/'
        cls.client_data = {
            "name": "Another Client LLC",
            "email": "another@innovatebr.com",
            "phones": [{"phone_number": "987654321"}],
            "addresses": [{"address_line": "456 Another St", "city": "Anotherville", "postal_code": "67890"}]
        }


    def setUp(self):
        url_token = '/api/token/'

        body_token = {
            "username": "",
            "password": ""
        }

        token_resp = self.client.post(url_token , body_token , format='json')

        self.assertEqual(token_resp.status_code , status.HTTP_200_OK )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_resp.data['access'])

    def test_create_client(self):

        resp = self.client.post(self.client_url , self.client_data , format='json')

        self.assertEqual(resp.status_code , status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count() , 1)
        self.assertEqual(Client.objects.get().name , 'Another Client LLC')


'''
how to use mock ????

from unittest.mock import patch

# ... inside your ClientAPITests class
    @patch('crudEx.views.send_welcome_email') # Path to where the function is USED
    def test_create_client_sends_welcome_email(self, mock_send_email):
        """
        Ensure the welcome email function is called when a client is created.
        """
        url = '/api/clients/'
        data = {"name": "Mock Client", "email": "mock@innovatebr.com", "phones": [], "addresses": []}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert that our mocked function was called exactly once
        mock_send_email.assert_called_once()
        # You can even check WHAT it was called with
        mock_send_email.assert_called_with("mock@innovatebr.com")
'''