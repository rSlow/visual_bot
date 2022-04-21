from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sql_urls import DATABASE_URL
import logging
from sqlalchemy import select

Engine = create_async_engine(DATABASE_URL)
Session = sessionmaker(bind=Engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class QueuePost(Base):
    __tablename__ = "queue_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    user_mention = Column(String)
    device = Column(String)
    photo_editing = Column(String)
    place = Column(String)
    image_ids = relationship("ImageID", cascade="all, delete, delete-orphan")

    @classmethod
    async def add_post(cls, post):
        logging.info("Appended post")
        async with Session() as session:
            async with session.begin():
                session.add(cls(
                    user_id=post.user_id,
                    user_mention=post.mention,
                    device=post.device,
                    photo_editing=post.photo_editing,
                    place=post.place,
                    image_ids=[ImageID(image_id=image_id) for image_id in post.image_ids]
                ))

    @classmethod
    async def get_all_posts(cls, session):
        result = await session.execute(select(cls).order_by(cls.id).options(selectinload(cls.image_ids)))
        return result.scalars().all()

    @classmethod
    async def delete_post_by_id(cls, session, post_id: int):
        result = await session.execute(select(cls).filter(cls.id == post_id))
        await session.delete(result.scalars().one())

    @classmethod
    async def update_post(cls, post):
        async with Session() as session:
            async with session.begin():
                result = await session.execute(
                    select(cls).filter(cls.id == post.id).options(selectinload(cls.image_ids))
                )
                orm_post = result.scalars().one()
                orm_post.device = post.device
                orm_post.photo_editing = post.photo_editing
                orm_post.place = post.place
                orm_post.image_ids = [ImageID(image_id=image_id, post_id=post.id) for image_id in post.image_ids]

    @classmethod
    async def get_image_orm_list(cls, session, post_id: int) -> list:
        result = await session.execute(select(cls).filter(cls.id == post_id))
        return result.one().image_ids


class ImageID(Base):
    __tablename__ = "image_ids"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("queue_posts.id"))
    image_id = Column(String)
