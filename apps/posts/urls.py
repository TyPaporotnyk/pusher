from django.urls import path

from . import views

urlpatterns = [
    # path("", views.PostView.as_view({"get": "list"}), name="posts"),
    path("", views.PostCreateView.as_view({"post": "create"}), name="create_post"),
    # path("<int:pk>/", views.PostView.as_view({"get": "list"}), name="post"),
    path("matches/", views.UserPostView.as_view({"get": "list"}), name="match_posts"),
    path("matches/<int:pk>/", views.UserPostView.as_view({"get": "retrieve"}), name="match_post"),
]
