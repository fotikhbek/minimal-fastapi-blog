from datetime import datetime
from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.schema import ForeignKey
from database.database import Base
from users.models import *


class Posts(Base):
    __tablename__ = 'posts'


    id = mapped_column(Integer, primary_key=True)
    header = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    posted_at = mapped_column(TIMESTAMP, default=datetime.utcnow)
    author = mapped_column(ForeignKey('users.username'), nullable=False)
    owner = relationship("Users", back_populates="posts")
