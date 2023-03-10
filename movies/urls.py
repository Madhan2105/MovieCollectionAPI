from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.Movies.as_view(), name='movies'),
    path('register/', views.User.as_view(), name='register'),
    path('collection/', views.Collection.as_view(), name='collection'),
    path('collection/<str:pk>', views.Collection.as_view(),
         name='collection_id'),
]
