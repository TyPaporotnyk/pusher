from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryView.as_view({"get": "list"}), name="categories"),
    path("categories/<int:pk>/", views.CategoryView.as_view({"get": "retrieve"}), name="category"),
    path("groups/", views.GroupView.as_view({"get": "list"}), name="groups"),
    path("groups/<int:pk>/", views.GroupView.as_view({"get": "retrieve"}), name="group"),
    path("keywords/", views.KeywordView.as_view({"get": "list"}), name="keywords"),
    path("keywords/<int:pk>/", views.KeywordView.as_view({"get": "retrieve"}), name="keyword"),
    # path("blacklists/", views.BlackListView.as_view({"get": "list"}), name="blacklists"),
    # path("blacklist/<int:pk>/", views.BlackListView.as_view({"get": "retrieve"}), name="blacklist"),
]
