import re
from dataclasses import dataclass, field
from typing import List

from apps.common.models import Keyword
from apps.customers.services.customers import BaseCustomerService
from apps.posts.models import Post


@dataclass
class CustomerPostMatchFilter:
    customer_service: BaseCustomerService
    keyword_match_result: List[Keyword] = field(default_factory=list)

    def is_valid(self, post: Post) -> bool:
        return (
            self._check_post_by_keyword(post)
            and self._check_post_by_groups(post)
            and not self._check_post_by_blacklist(post)
        )

    def _check_post_by_keyword(self, post: Post) -> bool:
        keywords = self.customer_service.keyword_service.get_all(active=True)
        keyword_match = [
            keyword
            for keyword in keywords
            if re.search(r"\b" + re.escape(keyword.name.lower()) + r"\b", post.description.lower())
        ]
        self.keyword_match_result = keyword_match
        return bool(keyword_match)

    def _check_post_by_groups(self, post: Post) -> bool:
        groups = self.customer_service.group_service.get_all(active=True)
        group_urls = {group.url for group in groups}
        return post.group_url in group_urls

    def _check_post_by_blacklist(self, post: Post) -> bool:
        black_list = self.customer_service.black_list_service.get_all(active=True)
        black_list_keywords = {bad_keyword.name.lower() for bad_keyword in black_list}
        return any(bad_keyword in post.description.lower() for bad_keyword in black_list_keywords)
