from apps.base.repository import Repository
from apps.posts.models import Post


class PostRepository(Repository[Post]):
    model = Post
