from django.urls import path

from . import views

urlpatterns = [
    path(
        "me/",
        views.CustomerOwnerViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="customer-owner",
    ),
]
