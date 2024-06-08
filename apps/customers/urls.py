from django.urls import path

from . import views

urlpatterns = [
    path("", views.CustomerView.as_view({"get": "retrieve", "put": "update"}), name="index"),
]
