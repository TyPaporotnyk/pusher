from rest_framework import viewsets

from apps.common.pagination import Pagination
from apps.posts.models import Post
from apps.posts.repository import PostRepository
from apps.posts.serializers import PostSerializer
from apps.posts.services import PostService


class PostView(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.prefetch_related("images").order_by("-created_at")
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        post_service = PostService(post_repository=PostRepository())
        return post_service.get_all_posts()
