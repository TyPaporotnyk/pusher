from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserPostView.as_view({"get": "list"}), name="get_products"),
    path("<int:pk>/", views.PostView.as_view({"get": "retrieve"}), name="get_product"),
]
