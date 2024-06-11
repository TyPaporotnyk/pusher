import pytest

from apps.posts.services import BasePostService
from tests.factories.posts import PostModelFactory


@pytest.mark.django_db
def test_get_posts_all(post_service: BasePostService):
    expected_count = 5
    posts = PostModelFactory.create_batch(size=expected_count)
    post_titles = {post.title for post in posts}

    fetched_posts = post_service.get_all_posts()
    fetched_titles = {post.title for post in fetched_posts}

    assert len(fetched_titles) == expected_count, f"{fetched_titles=}"
    assert post_titles == fetched_titles, f"{post_titles=}"
