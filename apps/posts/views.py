from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser

from apps.base.pagination import Pagination
from apps.posts.repository import PostRepository
from apps.posts.serializers import MatchPostSerializer, PostCreateSerializer, PostSerializer
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
    serializer_class = MatchPostSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        last_post_id = self.request.query_params.get("last_post_id", None)
        ordering = self.request.query_params.get("ordering", "-created_at")

        posts = user.matched_posts.all().order_by(ordering).select_related("post").prefetch_related("keywords")

        if last_post_id is not None:
            if "-" in ordering:
                posts = posts.filter(id__lt=last_post_id)
            else:
                posts = posts.filter(id__gt=last_post_id)

        return posts
