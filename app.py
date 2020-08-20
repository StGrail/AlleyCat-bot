from loader import db
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify
    try:
        await db.create_table_racers()
    except Exception as e:
        print('err')
    await db.delete_racers()
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)