from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Meme(Base):
    __tablename__ = 'memes'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    hash = Column(String(150), unique=True)
    tags = relationship('Tag', backref='meme', single_parent=True, cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(50), unique=False)
    meme_id = Column(Integer, ForeignKey('memes.id'), unique=False, nullable=False)
