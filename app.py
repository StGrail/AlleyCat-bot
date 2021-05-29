from aiogram import types

from handlers.command_info import send_mechanic
from utils.loader import db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    try:
        await db.create_table_racers()
    except:
        pass

    await on_startup_notify(dp)
    await set_default_commands(dp)
    try:
        await send_mechanic(types.Message)
    except:
        pass


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
