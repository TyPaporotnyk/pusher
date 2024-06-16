from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.CustomerView.as_view({"get": "retrieve"}), name="customer"),
    path("me/update/", views.UpdateCustomerView.as_view(), name="customer"),
    path("groups/", views.CustomerGroupView.as_view({"get": "list", "post": "create"}), name="customer-groups"),
    path("keywords/", views.CustomerKeywordView.as_view({"get": "list", "post": "create"}), name="customer-keywords"),
    # path(
    #     "blacklists/",
    #     views.CustomerBlackListView.as_view({"get": "list", "post": "create"}),
    #     name="customer-blacklists",
    # ),
    path("posts/", views.CustomerPostView.as_view({"get": "list"}), name="match-posts"),
    path("posts/<int:pk>/", views.CustomerPostView.as_view({"get": "retrieve"}), name="match-post"),
    path("telegram/", views.CustomerTelegramView.as_view({"get": "retrieve", "post": "update"}), name="telegram"),
]
