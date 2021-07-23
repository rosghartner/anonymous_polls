from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Poll



class PollsTests(APITestCase):
    """Тестирование"""

    @classmethod
    def setUpTestData(cls):

        user_test1 = User.objects.create_user(username='test', password='use12345')
        user_test1.save()
        cls.user_test1_token = Token.objects.create(user=user_test1)
        cls.poll_data = {
            "title": "test1_poll_title",
            "creator": 1,
            "description": "test1_poll_description",
            "questions": [
                {
                "question": "test1_question1",
                "answers": [
                    {
                    "answer": "test1_answer1"
                    },
                    {
                    "answer": "test1_answer2"
                    }
                ]
                },
                {
                "question": "test1_question2",
                "answers": [
                    {
                    "answer": "test1_answer3"
                    },
                    {
                    "answer": "test1_answer4"
                    }
                ]
                }
            ]
        }
        cls.one_poll = Poll.objects.create(
            creator = user_test1,
            title = 'test',
            description = 'description',
        )

    def setUp(self):
        # user_test1 = User.objects.create_user(username='test', password='use12345')
        # user_test1.save()
        # self.user_test1_token = Token.objects.create(user=user_test1)
        pass

    def test_poll_list_invalid_auth(self):
        response = self.client.get(reverse('poll_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_poll_list_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse('poll_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_poll_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(reverse('create_poll'), self.poll_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_poll_invalid_auth(self):
        response = self.client.post(reverse('create_poll'), self.poll_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_poll_id_invalid_auth(self):
        response = self.client.get(reverse('poll_id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_poll_id_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(reverse('poll_id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'************{response.data}***********')
