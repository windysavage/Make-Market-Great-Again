from datetime import datetime

import attr
from truthbrush.api import Api as TruthApi

from settings import get_settings
from utils import ensure_datetime_type

settings = get_settings()
truth_api = TruthApi(
    username=settings.TRUTHSOCIAL_USERNAME,
    password=settings.TRUTHSOCIAL_PASSWORD,
)


@attr.s(repr=True, frozen=True)
class Post:
    content: str = attr.ib()
    created_at: str = attr.ib()


def is_valid_page(page: dict) -> bool:
    if not page or 'content' not in page:
        return False
    if page['content'] == '<p></p>':
        return False
    return True


def pull_user_post(
    username: str,
    created_after: str | datetime,
    replies: bool = False,
    pinned: bool = False,
) -> list[Post]:
    created_after = ensure_datetime_type(created_after)
    return [
        Post(content=page.get('content'), created_at=page.get('created_at'))
        for page in truth_api.pull_statuses(
            username, created_after=created_after, replies=replies, pinned=pinned
        )
        if is_valid_page(page)
    ]


if __name__ == '__main__':
    print(
        pull_user_post(
            username='realDonaldTrump',
            created_after='2025-07-08-12-00',
        )
    )
