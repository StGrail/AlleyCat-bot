WELCOME_MESSAGE = '''
<b>Добро пожаловать на CyberAlleycat</b>!

В прошлом году мы первыми в России провели <a href='vk.com/cyberalleycat'>кибер-аллейкат</a>.
В этом году мы решили не пренебрегать рекомендациями ВОЗ и
предлагаем вам улучшенный формат бесконтакной гонки (почти как ApplePay).

На нашей гонки нет привычных для всех атрибутов:

- никаких толп на месте старта;
- ничего не нужно передавать волонтерам на точках;
- да и сами волонтеры совсем не нужны;
- мы призываем держать дистанцию и не сидеть друг у друга на колесе!

Перейдем к правилам гонки:
'''

START_INFO = '''
Сбор в 12.00
Начало гонки ровно в 12.10\n
Место старта гонки:\n
<code>Устьинский сквер, Памятник Пограничникам Отечества</code>\n
Перед стартом, тебе придет сообщение от бота, так что <b>не выключай</b> оповещения.
'''

RULES = '''
Гонка состоит из 8 точек, не считая точки старта.\n
На каждой точке вам нужно отправить локацию с телефона и для подверждения - отправить селфи или фото \
велосипеда с объектом на заднем фоне.\n
Для избежания неточностей отправдления локации с телефона, следует останавливаться и уже после отправлять локацию.\n
Если у вас <b>не айфон</b>, то можно копировать название точки по нажатию на текст, как на этом примере:\n
<code>Улица Пушкина, дом Колотушкина</code>\n
Таким образом, быстро копируется название точки и ее удобно вставлять его в поиске на картах.\n
В остальном - это обычный аллейкат, так что отправляй ссылку друзьям и переходи к регистрации.
'''

# Fan things for answers
dont_write_to_me = [
    '''
    — Привет, я подсяду? Спасибо.
    — Почему у меня велосипед без тормозов? Ну, просто мне понравился парень.
    — Поддерживаю ли я МГБТ? Да.
    — Да, я являюсь частью сообщества. А почему ты спрашиваешь?
    — В смысле навязываю тебе что-то? Так ты же сам спросил. Ладно.
    — Хочу ли я свою подругу? Боже, нет, конечно. Почему я должен её хотеть?
    — В смысле всех? Нет, постой, это не так работает немножко. Тебе объяснить?
    — Не надо пропагандировать? Я не пропагандирую, ты просто сам спросил у меня… 
    - Ясно, я сумасшедший. Как и все. Ладно, извини, что потревожил. Я отсяду.
    ''',
    'Не пиши мне больше!',
    'Лучше отправь голосовое',
]

audio_answer = [
    'Я без наушников, лучше напиши.',
    'Пожалуйста, повтори еще раз.',
    'Тебя не слышно, говори громче.',
]
