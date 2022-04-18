from typing import Optional


class PostSchema:
    image_id: str
    device: str
    photo_editing: Optional[str]
    place: str

    def __init__(self, user_id):
        self.user_id = user_id
