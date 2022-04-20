from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from sql_urls import DATABASE_URL
import logging

Engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()


class QueuePost(Base):
    __tablename__ = "queue_posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_mention = Column(String)
    device = Column(String)
    photo_editing = Column(String)
    place = Column(String)
    image_ids = relationship("ImageID", cascade="all, delete, delete-orphan")

    @classmethod
    def add_post(cls, post):
        logging.info("Appended post")
        with Session.begin() as session:
            session.add(cls(
                user_id=post.user_id,
                user_mention=post.mention,
                device=post.device,
                photo_editing=post.photo_editing,
                place=post.place,
                image_ids=[ImageID(image_id=image_id) for image_id in post.image_ids]))

    @classmethod
    def get_all_posts(cls, session):
        return session.query(cls).all()

    @classmethod
    def delete_post_by_id(cls, session, post_id: int):
        result = session.query(cls).filter(cls.id == post_id).one()
        session.delete(result)

    @classmethod
    def update_post(cls, post):
        with Session.begin() as session:
            result = session.query(cls).filter(cls.id == post.id).one()
            result.device = post.device
            result.photo_editing = post.photo_editing
            result.place = post.place
            result.image_ids = [ImageID(image_id=image_id, post_id=post.id) for image_id in post.image_ids]

    @classmethod
    def get_image_orm_list(cls, session, post_id: int) -> list:
        return session.query(cls).filter(cls.id == post_id).one().image_ids


class ImageID(Base):
    __tablename__ = "image_ids"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("queue_posts.id"))
    image_id = Column(String)
