from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostCreateView.as_view({"post": "create"}), name="create-post"),
]
