from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from flask_login import UserMixin
import backend
from backend import db
from typing import Optional, List

class User(UserMixin, db.Model):
    __table__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

class Language(db.Model):
    __table__ = "language"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    words: Mapped[List['Word']] = relationship('Word', cascade='all, delete-orphan', back_populates='language')
    lessons: Mapped[List['Lesson']] = relationship('Lesson', cascade='all, delete-orphan', back_populates='language')

class Word(db.Model):
    __table__ = "word"
    id: Mapped[int] = mapped_column(primary_key=True)
    lang_id: Mapped[int] = mapped_column(ForeignKey('language.id', ondelete='CASCADE'))
    language = relationship('Language', back_populates='words')
    english: Mapped[str]
    translation: Mapped[str]
    definition: Mapped[Optional[str]]

# very basic lesson format of title and text
# images can be embedded in lesson Markdown style
class Lesson(db.Model):
    __table__ = "lesson"
    id: Mapped[int] = mapped_column(primary_key=True)
    lang_id: Mapped[int] = mapped_column(ForeignKey('language.id', ondelete='CASCADE'))
    language = relationship('Language', back_populates='lessons')
    title: Mapped[str]
    text: Mapped[str]
    