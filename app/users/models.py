
from sqlalchemy import Integer, String,Boolean,LargeBinary
from sqlalchemy.orm import relationship, mapped_column
from database.database import Base
from posts.models import *
import uuid

class Users(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False, unique=True)
    hashed_password = mapped_column(LargeBinary, nullable=False)
    is_active = mapped_column(Boolean, default=True)
    is_superuser = mapped_column(Boolean, default=False)
    posts = relationship("Posts", back_populates="owner")

