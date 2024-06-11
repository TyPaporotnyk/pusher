from dataclasses import dataclass, field

from apps.customers.models import Customer
from apps.posts.models import Post


@dataclass
class CustomerPostMatchFilter:
    customer: Customer
    keyword_match_result: list[str] = field(default_factory=list)

    def is_valid(self, post: Post) -> bool:
        return (
            self._check_post_by_keyword(post)
            and self._check_post_by_groups(post)
            and not self._check_post_by_blacklist(post)
        )

    def _check_post_by_keyword(self, post: Post) -> bool:
        group_keywords = self.customer.groups_keywords.all()
        if not group_keywords:
            return True

        keyword_match = [keyword.name in post.description for keyword in group_keywords]
        self.keyword_match_result = [item[0] for item in zip(group_keywords, keyword_match) if item[1]]

        return any(keyword_match)

    def _check_post_by_groups(self, post: Post) -> bool:
        groups = self.customer.groups.all()
        if not groups:
            return True

        return any([group.url == post.group_url for group in groups])

    def _check_post_by_blacklist(self, post: Post) -> bool:
        black_list = self.customer.blacklist.all()
        if not black_list:
            return False

        return any([bad_keyword.name in post.description for bad_keyword in self.customer.blacklist.all()])
