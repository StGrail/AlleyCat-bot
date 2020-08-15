import time

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from FSM.Race_states import Race
from FSM.Registation_states import Registration_form
from keyboards.inline_kb import bicycle_type, gender, apply_registration, check_reg_answer, are_you_ready
from loader import dp

'''Создать хендлеры группу коллбэков для каждого состояния'''

rule = '''Нельзя ехать на машине
Можно ехать на велосипеде и тд
Я согласен с условиями и готов регистрироваться'''


# нажатие кнопки правила
@dp.callback_query_handler(text='rules')
async def rules(call: CallbackQuery):
    await call.answer(cache_time=55)
    await call.message.edit_text(f'{rule}', reply_markup=apply_registration)


# нажатие кнопки "Регистрация"
@dp.callback_query_handler(text='start_reg')
async def reg(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'Привет {call.from_user.full_name}, укажи свой пол:',
                                 reply_markup=gender)
    await Registration_form.Sex.set()  # добавить имя пользоваиеля и @name в бд


# выбор пола и кнопка выбора велосипеда
@dp.callback_query_handler(state=Registration_form.Sex)
async def choose_sex(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    answer = call.data
    await state.update_data(sex=answer)
    await call.message.edit_text(f'В какой категории участвуешь?', reply_markup=bicycle_type)
    await Registration_form.next()  # добавть пол в бд


# выбор категории велосипеда кнопки выбора проверки ответов
@dp.callback_query_handler(state=Registration_form.Bicycle_type)
async def choose_bicycle_type(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    answer = call.data
    await state.update_data(bicycle_type=answer)
    data = await state.get_data()
    if data.get('sex') == 'male':
        sex = 'Ты выбрал'
    elif data.get('sex') == 'female':
        sex = 'Ты выбрала'
    else:
        sex = 'Ты еще не определился с полом (участвуешь вне зачета) и выбрал'

    if call.data == 'fixie':
        bicycle = 'фиксы 🚲'
    else:
        bicycle = 'мульти/синглспид 🚴'

    await call.message.edit_text(f'{sex} категорию: {bicycle}', reply_markup=check_reg_answer)
    await state.reset_state(with_data=False)  # занести все в бд


# исправление ошибок при регистрации
@dp.callback_query_handler(text='data_not_ok')
async def pravki(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.reset_data()
    await state.reset_state()
    await call.message.edit_text('Укажи еще раз свой пол:', reply_markup=gender)
    await Registration_form.Sex.set()


# информация о месте старта
@dp.callback_query_handler(text='data_ok')
async def waiting_start(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='''
Отлично, старт гонки - Изваринская ул, дом 1.
Начало гонки 1го сентября в 12.10.
Перед стартом, тебе придет сообщение от бота, так что не выключай оповещения.
Не приезжай на точку старта слишком рано и пользуйся санитайзером.''')
    time.sleep(3)  # изменить на date и поставить "будильник" до конца недели
    await call.message.delete()
    await call.message.answer('Ты готов к гонке?', reply_markup=are_you_ready)
    await Race.First_point.set()
