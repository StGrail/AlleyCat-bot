from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('help', 'Жми, если не можешь отправить локацию'),
        types.BotCommand('racers', 'Посмотреть всех участников гонки'),
        types.BotCommand('info', 'Дополнительная информация о гонке'),
    ])
