# Как работает этот декоратор:
# connection принимает исходную функцию для обёртки.
# wrapper — это функция-обёртка, которая принимает все аргументы исходной функции.
# async with async_session_maker() автоматически создаёт и закрывает сессию в асинхронном режиме, 
# освобождая вас от необходимости управлять сессией вручную.
# Сессия передаётся в исходную функцию через аргумент session.
# В случае ошибки выполняется откат транзакции через rollback(), а затем сессия закрывается.

from db.database import async_session_maker

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper