from django.urls import path

from . import views

urlpatterns = [
    # path("", views.CustomerView.as_view({"get": "list"}), name="customers"),
    # path("<int:pk>/", views.CustomerView.as_view({"get": "retrieve", "put": "update"}), name="customer"),
    path(
        "me/",
        views.CustomerOwnerViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="customer-owner",
    ),
]
