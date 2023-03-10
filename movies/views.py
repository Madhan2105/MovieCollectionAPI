from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
from .utility import CustomSession
import os
from rest_framework import status
from .serializer import CollectionSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Collection as CollectionModel
from django.http import Http404
from datetime import datetime
load_dotenv()


class Movies(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        page = "?page="+request.query_params.get('page') \
            if request.query_params.get('page') else ""
        with CustomSession("https://demo.credy.in/", os.getenv('APIUsername'),
                           os.getenv('APIPassword')) as session:
            try:
                resp = session.get("https://demo.credy.in/api/v1/maya/movies/"
                                   + page)
            except ConnectionError as ce:
                return Response(ce, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(resp.json(), status=resp.status_code)


class User(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Collection(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return CollectionModel.objects.get(id=pk, is_active=1)
        except CollectionModel.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if (pk):
            collection = self.get_object(pk)
            serializer = CollectionSerializer(collection)
        else:
            context = {"show_fav_genres": True}
            u = request.user
            collection = CollectionModel.objects.filter(collection_user=u.id,
                                                        is_active=1)
            serializer = CollectionSerializer(collection, many=True,
                                              context=context)
        return Response(serializer.data)

    def post(self, request, format=None):
        u = request.user
        context = {"show_only_collection_id": True}
        serializer = CollectionSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(collection_user=u, created_by=u.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        movies = self.get_object(pk)
        u = request.user
        serializer = CollectionSerializer(movies, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=u.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.is_active = 0
        snippet.deleted_at = datetime.now()
        snippet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
