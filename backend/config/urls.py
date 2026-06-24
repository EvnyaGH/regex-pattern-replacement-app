"""URL configuration for the backend project."""

from django.urls import path

from api.router import api


urlpatterns = [
    path("api/", api.urls),
]
