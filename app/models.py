from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "user" #This table needs to be renamed to 'users' and will affect the user.whatever on this file
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #This column should  be renamed to 'registered_at'

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)