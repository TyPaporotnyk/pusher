import pytest

from apps.posts.repository import PostRepository
from apps.posts.services import BasePostService, PostService


@pytest.fixture
def post_service() -> BasePostService:
    post_repository = PostRepository()
    return PostService(post_repository=post_repository)
