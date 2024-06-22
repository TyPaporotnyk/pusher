from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.CustomerView.as_view({"get": "retrieve", "patch": "partial_update"})),
    path("groups/", views.CustomerGroupView.as_view({"get": "list", "post": "create"})),
    path("keywords/", views.CustomerKeywordView.as_view({"get": "list", "post": "create"})),
    path("blacklists/", views.CustomerBlackListView.as_view({"get": "list", "post": "create"})),
    path("posts/", views.CustomerPostView.as_view({"get": "list"})),
    path("posts/<int:pk>/", views.CustomerPostView.as_view({"get": "retrieve"})),
    path("telegram/", views.CustomerTelegramView.as_view({"get": "retrieve", "post": "update"})),
]
