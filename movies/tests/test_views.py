from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from movies.models import Collection
from .. import views
from django.contrib.auth.models import User
from .factory import CollectionFactory, UserFactory


class MoviesTest(APITestCase):
    def test_get_movies(self):
        """
            Ensure all the movies data is fetched
        """
        url = reverse('movies')
        factory = APIRequestFactory()
        view = views.Movies.as_view()
        request = factory.get(url)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movies_using_page_number(self):
        """
            Ensure all the movies data is fetched using page number
        """
        url = reverse('movies')
        factory = APIRequestFactory()
        view = views.Movies.as_view()
        request = factory.get(url+"?page=2")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movies_using_invalid_page_number(self):
        """
            Ensure it throws valid error when page number is invalid
        """
        url = reverse('movies')
        factory = APIRequestFactory()
        view = views.Movies.as_view()
        request = factory.get(url+"?page=22222")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserTest(APITestCase):
    def test_create_user(self):
        """
            Ensure we can create user
        """
        factory = APIRequestFactory()
        view = views.User.as_view()
        url = reverse('register')
        data = {
            "username": "madhan_nadar12234",
            "password": "mynameIS@03"
        }
        request = factory.post(url, data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CollectionTest(APITestCase):
    def createUser(self):
        view = views.User.as_view()
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
        self.view = views.Collection.as_view()
        self.factory = APIRequestFactory()

    def test_create_collection(self):
        """
            Ensure we can create a new collecion.
        """
        data = {
            "title": "my collection 2",
            "description": "Fav move last summer",
            "movies": [
                {
                    "title": "Betrayal",
                    "description": """When one of her hits goes wrong, a
                      professional assassin ends up with a suitcase full of
                      a million dollars belonging to a mob boss ...""",
                    "genres": "Action,Drama,Thriller",
                    "uuid": "720e8796-5397-4e81-9bd7-763789463707"
                }
            ]
        }
        url = reverse('collection')
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collection.objects.filter(is_active=1).count(), 1)
        self.assertEqual(Collection.objects.get().title, 'my collection 2')
        self.assertEqual(str(Collection.objects.get().id),
                         str(response.data["collection_uuid"]))
        return str(response.data["collection_uuid"])

    def test_get_all_collections(self):
        """
            Ensure we are ale to fetch collection.
        """
        CollectionFactory.create_batch(10)
        url = reverse('collection')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Collection.objects.filter(is_active=1).count(), 10)

    def test_get_empty_collections(self):
        """
            Ensure we are ale to fetch empty collection.
        """
        url = reverse('collection')
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Collection.objects.filter(is_active=1).count(), 0)
        self.assertEqual(response.data, [])

    def test_get_collection(self):
        """
            Ensure we are able to fetch collection on basis of collection id.
        """
        collection = CollectionFactory()
        collection_id = str(collection.id)
        url = reverse('collection')
        request = self.factory.get(url+"/"+collection_id)
        force_authenticate(request, user=self.user)
        response = self.view(request, collection_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Collection.objects.filter(is_active=1).count(), 1)
        self.assertEqual(response.data['id'], collection_id)

    def test_update_collection(self):
        """
            Ensure we are ale to update collection.
        """
        collection = CollectionFactory()
        data = {
            "title": collection.title,
            "description": collection.description,
            "movies": collection.movies
        }
        collection_id = str(collection.id)
        url = reverse('collection')
        request = self.factory.put(url+"/"+collection_id,
                                   data=data, format="json")
        force_authenticate(request, user=self.user)
        response = self.view(request, collection_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Collection.objects.filter(is_active=1).count(), 1)
        self.assertEqual(response.data['id'], collection_id)

    def test_delete_collection(self):
        """
            Ensure we can delete collection
        """
        collection = CollectionFactory()
        collection_id = str(collection.id)
        url = reverse('collection')
        request = self.factory.delete(url+"/"+collection_id)
        force_authenticate(request, user=self.user)
        response = self.view(request, collection_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.filter(is_active=1).count(), 0)

    def test_get_collection_unauthorized(self):
        """
            Ensure we are thrown error when request is unauthorized.
        """
        collection = CollectionFactory()
        collection_id = str(collection.id)
        url = reverse('collection')
        request = self.factory.get(url+"/"+collection_id)
        response = self.view(request, collection_id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
