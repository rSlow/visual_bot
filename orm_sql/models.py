from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from schemas import PostSchema

from sql_urls import DATABASE_URL

Engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()


class QueuePost(Base):
    __tablename__ = "queue_posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    image_id = Column(String)
    device = Column(String)
    photo_editing = Column(String)
    place = Column(String)

    @classmethod
    def add_post(cls, post_schema):
        with Session.begin() as session:
            session.add(cls(
                user_id=post_schema.user_id,
                image_id=post_schema.image_id,
                device=post_schema.device,
                photo_editing=post_schema.photo_editing,
                place=post_schema.place))

    @classmethod
    def get_user_posts(cls, user_id):
        with Session.begin() as session:
            return session.query(cls).filter(user_id=user_id).all()

    @classmethod
    def delete_post(cls, post_id):
        with Session.begin() as session:
            post = session.query(cls).filter(id=post_id).one()
            session.delete(post)
