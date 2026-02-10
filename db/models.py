from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, BigInteger
from db.database import Base



class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    tg_name: Mapped[str]
    tg_username: Mapped[str]
    tg_number: Mapped[str]


class Profile(Base):

    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    count_game: Mapped[int] = mapped_column(default=0)
    winner_game: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))

