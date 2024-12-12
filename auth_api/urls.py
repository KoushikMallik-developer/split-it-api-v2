from django.urls import path
from .views import EnvRead

urlpatterns = [
    path("env_data/", EnvRead.as_view(), name="test_endpoint"),
]
