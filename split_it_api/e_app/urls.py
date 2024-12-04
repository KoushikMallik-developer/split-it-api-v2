from django.urls import path
from .views import TestView


urlpatterns = [
    path('endpoint/', TestView.as_view(), name='test_endpoint'),
]