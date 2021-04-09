from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from FSM.Race_states import Race
from constants.locations import points
from keyboards.inline_kb import got_the_point
from keyboards.reply_kb import get_location_button, remove_keyboard
from utils.loader import dp, db


# запрос локации на точке старта
@dp.callback_query_handler(state=Race.FIRST_POINT)
async def get_location(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    await call.message.delete()
    await call.message.answer('Отправь своё местоположение 🗺.\nКнопка снизу ⬇️',
                              reply_markup=get_location_button)
    await state.reset_state()


# уловитель локации и сортировка по самой локации
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def selfie_query(message: types.Message, state: FSMContext):
    on_point = 'Ты на месте!\nДля подтверждения, отправь селфи 📷'
    user_latitude = float(f'{message.location["latitude"]:.5f}')
    user_longitude = float(f'{message.location["longitude"]:.5f}')
    R = 0.0005  # Зона действия вокруг точки - 50 метров

    if (user_latitude - points['Start']['latitude']) ** 2 + \
            (user_longitude - points['Start']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.CHRIST_THE_SAVIOR.set()
    elif (user_latitude - points['2nd']['latitude']) ** 2 + \
            (user_longitude - points['2nd']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.CATHOLIC_CATHEDRAL.set()
    elif (user_latitude - points['3rd']['latitude']) ** 2 + \
            (user_longitude - points['3rd']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.ALLAAH.set()
    elif (user_latitude - points['4th']['latitude']) ** 2 + \
            (user_longitude - points['4th']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.SEYNAGOGUE.set()
    elif (user_latitude - points['5th']['latitude']) ** 2 + \
            (user_longitude - points['5th']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.EVANGELICAL.set()
    elif (user_latitude - points['6th']['latitude']) ** 2 + \
            (user_longitude - points['6th']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.SCIENTOLOGY.set()
    elif (user_latitude - points['7th']['latitude']) ** 2 + \
            (user_longitude - points['7th']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.MOSGORBIKE.set()
    elif (user_latitude - points['Finish']['latitude']) ** 2 + \
            (user_longitude - points['Finish']['longitude']) ** 2 <= R ** 2:
        await message.answer(on_point)
        await Race.FINISH.set()
    else:
        await message.answer('Ты далеко от точки, попробуй еще раз', reply_markup=get_location_button)


# подверждение фото со стейтами
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.CHRIST_THE_SAVIOR)
async def got_selfie_christ(message: types.Message, state: FSMContext):
    await state.reset_state()
    start_time = datetime.now().strftime('%H:%M:%S')
    await db.start_time(start_time=start_time, id=message.from_user.id)
    await message.answer('Отличная фотография, первая точка:\n\n'
                         '<code>Церковь Спаса Преображения в комплексе храма Христа Спасителя</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.CATHOLIC_CATHEDRAL)
async def got_selfie_catholic(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Отличная фотка, дуй на следующую точку:\n\n'
                         '<code>Римско-католический Кафедральный собор Непорочного Зачатия Пресвятой Девы Марии</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.ALLAAH)
async def got_selfie_allah(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Езжай на следующую точку:\n\n'
                         '<code>Московская соборная мечеть</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.SEYNAGOGUE)
async def got_selfie_seynagogue(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Отличная фотка, дуй на следующую точку:\n\n'
                         '<code>Московская хоральная синагога</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.EVANGELICAL)
async def got_selfie_evangelical(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Отличная фотка, дуй на следующую точку:\n\n'
                         '<code>Евангелическо-лютеранский кафедральный собор святых Петра и Павла</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.SCIENTOLOGY)
async def got_selfie_scientology(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Отличная фотка, дуй на следующую точку:\n\n'
                         '<code>Московская саентологическая церковь</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.MOSGORBIKE)
async def got_selfie_mosgorbike(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Отличная фотка, дуй на следующую точку:\n'
                         '<code>Mosgorbike</code>',
                         reply_markup=got_the_point)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Race.FINISH)
async def got_selfie_finish(message: types.Message, state: FSMContext):
    """Финишное фото у мгб и расчет времени гонки"""

    await state.finish()
    time_start = await db.get_start_time(id=message.from_user.id)
    time_start = time_start[0]
    time_finish = datetime.now().strftime('%H:%M:%S')
    total_time = datetime.strptime(time_finish, '%H:%M:%S') - datetime.strptime(time_start, '%H:%M:%S')
    await db.finish_time(finish_time=time_finish, id=message.from_user.id)
    await db.total_time(total_time=str(total_time), id=message.from_user.id)

    await message.answer('Поздравляю, ты добрался до последней точки, готовься к награждению!',
                         reply_markup=remove_keyboard)
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEBNehfOYqypKm5tQW7ighPme49OflY7gACaAADq8pZIY2MuYKiZ0KSGgQ')


# запрос локации
@dp.callback_query_handler(text='got_the_point')
async def get_location(call: CallbackQuery):
    await call.answer(cache_time=3)
    await call.message.delete()
    await call.message.answer('Отправь своё местоположение 🗺\nКнопка снизу ⬇️',
                              reply_markup=get_location_button)
