from rest_framework import viewsets

from apps.common.pagination import Pagination
from apps.filters.services.customer import CustomerPostsFilter
from apps.posts.repository import PostRepository
from apps.posts.serializers import PostSerializer
from apps.posts.services import PostService


class PostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        post_service = PostService(post_repository=PostRepository())
        return post_service.get_all_posts()


class UserPostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        post_service = PostService(post_repository=PostRepository())
        all_new_posts = post_service.get_all_posts()
        customer_posts_filter = CustomerPostsFilter(customer=self.request.user)
        filtered_posts = customer_posts_filter.get_filtered_posts(all_new_posts)
        return filtered_posts
