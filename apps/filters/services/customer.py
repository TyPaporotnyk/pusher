from dataclasses import dataclass

from django.db.models import QuerySet

from apps.filters.services.base import BaseCustomerPostsFilter
from apps.posts.models import Post


@dataclass(kw_only=True)
class CustomerPostsFilter(BaseCustomerPostsFilter):

    def get_filtered_posts(self, posts: QuerySet[Post]) -> list[Post]:
        filtered_posts = [
            post
            for post in posts
            if self._check_post_by_keyword(post)
            and self._check_post_by_groups(post)
            and not self._check_post_by_blacklist(post)
        ]
        return filtered_posts

    def _check_post_by_keyword(self, post: Post) -> bool:
        group_keywords = self.customer.groups_keywords.all()
        if not group_keywords:
            return True

        return any([keyword.name in post.description for keyword in group_keywords])

    def _check_post_by_groups(self, post: Post) -> bool:
        groups = self.customer.groups.all()
        if not groups:
            return True

        return any([group.url in post.url for group in groups])

    def _check_post_by_blacklist(self, post: Post) -> bool:
        black_list = self.customer.blacklist.all()
        if not black_list:
            return False

        return any([bad_keyword.name in post.description for bad_keyword in self.customer.blacklist.all()])
