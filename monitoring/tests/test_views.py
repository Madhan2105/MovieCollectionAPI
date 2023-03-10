from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from monitoring.models import Counter
from django.contrib.auth.models import User
from .. import views
from movies import views as movie_views
from movies.tests.factory import UserFactory


class CustomSetup(APITestCase):
    def createUser(self):
        view = movie_views.User.as_view()
        url = reverse('register')
        factory = APIRequestFactory()
        user_factory = UserFactory()
        data = {
            "username": user_factory.username,
            "password": user_factory.password
        }
        request = factory.post(url, data, format='json')
        view(request)
        return user_factory.username

    def setUp(self):
        username = self.createUser()
        self.user = User.objects.get(username=username)
        self.factory = APIRequestFactory()


class CounterTest(CustomSetup, APITestCase):
    def test_get_counter(self):
        """
            Ensure counter value is returned
        """
        url = reverse('request-counter')
        Counter.objects.create(id=1, request_count=1)
        view = views.Counter.as_view()
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requests'], 1)

    def test_get_counter_without_auth(self):
        """
            Ensure it throws error when it's not authorized
        """
        url = reverse('request-counter')
        Counter.objects.create(id=1, request_count=1)
        view = views.Counter.as_view()
        request = self.factory.get(url)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ResetCounterTest(CustomSetup, APITestCase):
    def test_reset(self):
        """
            Ensure the counter is reset
        """
        url = reverse('reset-counter')
        Counter.objects.create(id=1, request_count=1)
        view = views.Counter.as_view()
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_unauth_acess(self):
        """
            Ensure it throws error for unauthorized access.
        """
        url = reverse('reset-counter')
        Counter.objects.create(id=1, request_count=1)
        view = views.ResetCounter.as_view()
        request = self.factory.get(url)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
