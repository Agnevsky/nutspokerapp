from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from db.decorator import connection
from db.models import User


@connection
async def add_user(tg_id: int, tg_number: int, tg_name: str, tg_username: str, session):

    stmt = insert(User).values(
        tg_id=tg_id,
        tg_number=tg_number,
        tg_name=tg_name,
        tg_username=tg_username
    ).on_conflict_do_nothing(
        index_elements=["tg_id"]
    )

    await session.execute(stmt)
    await session.commit()


@connection
async def get_info(tg_id: int, session):

    result = await session.execute(select(User).where(User.tg_id == tg_id))

    return result.scalar_one_or_none()