from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from flask_login import UserMixin
import backend
from backend import db
from typing import Optional, List

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

class Language(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    words: Mapped[List['Word']] = relationship('Word', cascade='all, delete-orphan', back_populates='language')

class Word(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    lang_id: Mapped[int] = mapped_column(ForeignKey('language.id', ondelete='CASCADE'))
    language = relationship('Language', back_populates='words')
    english: Mapped[str]
    translation: Mapped[str]
    definition: Mapped[Optional[str]]