from typing import Optional, Union
from orm import QueuePost, Session
from aiogram.types import MediaGroup


class Post:
    id = None
    device: str
    photo_editing: Optional[str]
    place: str

    def __init__(self, user_id, mention):
        self.user_id = user_id
        self.mention = mention
        self.image_ids: list[str] = list()

    @property
    def text(self):
        text_block = f"{self.device} | {self.photo_editing or 'Clear'}" \
                     f"\n" \
                     f"-- {self.place}" \
                     f"\n" \
                     f'by <a href="tg://user?id={self.user_id}">{self.mention}</a>'
        return text_block

    @classmethod
    def from_orm_result(cls, result: QueuePost):
        post = cls(result.user_id, result.user_mention)
        post.id = result.id
        post.mention = result.user_mention
        post.device = result.device
        post.place = result.place
        post.image_ids = [orm.image_id for orm in result.image_ids]
        post.photo_editing = result.photo_editing
        return post

    def delete_photo(self, photo_num: int):
        del self.image_ids[photo_num - 1]

    def update(self):
        QueuePost.update_post(self)


class PostMediaGroup(MediaGroup):
    def __init__(self, *args, **kwargs):
        super(PostMediaGroup, self).__init__(*args, **kwargs)

    def attach_media_group(self, image_ids: list[str], group_caption: Optional[str] = None):
        self.attach_photo(image_ids[0], caption=group_caption)
        for image_id in image_ids[1:]:
            self.attach_photo(image_id)


class Queue(dict):
    def __init__(self, *args, **kwargs):
        super(Queue, self).__init__(*args, **kwargs)

    @classmethod
    def from_database(cls):
        with Session.begin() as session:
            results: list[QueuePost] = QueuePost.get_all_posts(session=session)
            return cls({post.id: post for post in [Post.from_orm_result(result) for result in results]})

    def get_first_post_id(self) -> int:
        for post_id in self:
            return post_id

    def get_first(self) -> Union[tuple[int, Post], tuple[None, None]]:
        post_id = self.get_first_post_id()
        if not post_id:
            return None, None
        post = self.get_post_by_id(post_id)
        return post_id, post

    def get_post_by_id(self, post_id) -> Post:
        return self[post_id]

    def delete_by_id(self, post_id) -> None:
        del self[post_id]
        with Session.begin() as session:
            QueuePost.delete_post_by_id(session=session, post_id=post_id)
