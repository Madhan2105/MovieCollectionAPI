from django.urls import path
from . import views

urlpatterns = [
    path('', views.Counter.as_view(), name='request-counter'),
    path('reset/', views.ResetCounter.as_view(), name='reset-counter'),
]
