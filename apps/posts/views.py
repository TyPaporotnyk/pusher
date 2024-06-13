from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser

from apps.base.pagination import Pagination
from apps.posts.repository import PostRepository
from apps.posts.serializers import PostCreateSerializer, PostSerializer
from apps.posts.services import PostService


@extend_schema(tags=["Posts"])
class PostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = Pagination
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        post_service = PostService(post_repository=PostRepository())
        return post_service.get_all_posts()


@extend_schema(tags=["Posts"])
class PostCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PostCreateSerializer
    permission_classes = (IsAdminUser,)


@extend_schema(tags=["Posts"])
class UserPostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        posts = self.request.user.matched_posts.all().order_by("-created_at").prefetch_related("images")
        return posts
