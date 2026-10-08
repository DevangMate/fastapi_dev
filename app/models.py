# Import the Base class you just created in database.py
from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from sqlalchemy import text,DateTime
from typing import List
class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    published: Mapped[bool] = mapped_column(server_default='TRUE', nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False, 
        server_default=text('now()')
    )
    owner_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="posts")

class User(Base):
    __tablename__ = "users"
    id:Mapped[int]=mapped_column(primary_key=True,nullable=False)
    email:Mapped[str]=mapped_column(nullable=False,unique=True)
    password:Mapped[str]=mapped_column(nullable=False)
    phone_number: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            nullable=False, 
            server_default=text('now()')
    )
    # A single user can have a list of many posts
    posts: Mapped[List["Post"]] = relationship(back_populates="owner")

class Vote(Base):
    __tablename__="votes"
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), 
        primary_key=True
    )