from django.test import TestCase
from rest_framework.test import APITestCase
from .factory import CollectionFactory, UserFactory
from ..serializer import CollectionSerializer, UserSerializer

class CollectionSerializerTest(APITestCase):
    def setUp(self):
        self.collection = CollectionFactory()
        self.collection_data = {
            "title": self.collection.title,
            "description":self.collection.description,
            "movies":self.collection.movies
        }


    def test_contains_expected_fields(self):
        """
            Ensure all the fields are returned by the Serializer
        """
        myfields = {'id', 'collection_user', 'created_by', 'updated_by', 'title', 'description', 'movies', 'created_at', 'updated_at', 'deleted_at', 'is_active'}
        self.serializer = CollectionSerializer(instance=self.collection)
        output_data = self.serializer.data
        self.assertEqual(set(output_data.keys()), myfields)

    def test_fav_genres_field_exist(self): 
        """
            Ensure favourite_genre field is also return when 
            'show_fav_genres' is passed in context.
        """       
        myfields = {'id', 'collection_user', 'created_by', 'updated_by', 'title', 'description', 'movies', 'created_at', 'updated_at', 'deleted_at', 'is_active', 'favourite_genres'}
        context = {"show_fav_genres": True}        
        self.serializer = CollectionSerializer(instance=self.collection, context=context)        
        output_data = self.serializer.data
        self.assertEqual(set(output_data.keys()), myfields)

    def test_serializer_collection_field_exist(self):
        context = {"show_only_collection_id": True}        
        self.serializer = CollectionSerializer(instance=self.collection, context=context)        
        output_data = self.serializer.data
        self.assertEqual(set(output_data.keys()), set(['collection_uuid']))


    def test_required_field_validation(self):
        self.collection_data.pop('title')
        self.serializer = CollectionSerializer(data=self.collection_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(set(self.serializer.errors.keys()),set(['title']))


    def test_invalid_title(self):
        """
            Ensure serializer throws error when the field level validation fails
        """
        self.collection_data['title'] = "s"
        self.serializer = CollectionSerializer(data=self.collection_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(set(self.serializer.errors.keys()),set(['title']))

class UserSerializerTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user_data = {
            "username":self.user.username,
            "password":self.user.password
        }   

    def test_contains_expected_fields(self):
        """
            Ensure all the fields are returned by the Serializer
        """
        myfields = {'access_token'}
        self.serializer = UserSerializer(instance=self.user)
        output_data = self.serializer.data
        self.assertEqual(set(output_data.keys()), myfields) 


    def test_missing_fields(self):
        """
            Ensure serializer throws error when the fields are missing
        """
        self.user_data.pop('username')
        self.serializer = UserSerializer(data=self.user_data)
        self.assertFalse(self.serializer.is_valid())
        self.assertEqual(set(self.serializer.errors.keys()),set(['username']))        
    