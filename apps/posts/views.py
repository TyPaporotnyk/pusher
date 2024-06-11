from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from apps.base.pagination import Pagination
from apps.customers.permissions import IsAdmin
from apps.filters.services.customer import CustomerPostsFilter
from apps.posts.repository import PostRepository
from apps.posts.serializers import PostSerializer
from apps.posts.services import PostService


@extend_schema(tags=["Posts"])
class PostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = Pagination
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        post_service = PostService(post_repository=PostRepository())
        return post_service.get_all_posts()


@extend_schema(tags=["Posts"])
class UserPostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        post_service = PostService(post_repository=PostRepository())
        all_new_posts = post_service.get_all_posts()
        customer_posts_filter = CustomerPostsFilter(customer=self.request.user)
        filtered_posts = customer_posts_filter.get_filtered_posts(all_new_posts)
        return filtered_posts
