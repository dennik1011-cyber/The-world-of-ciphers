import os
import random

from flask import Flask, render_template, request, redirect, make_response
from flask_login import login_user, login_required, logout_user, LoginManager

from ciphers import easy, normal
from data import db_session
from data.users import User
from forms.users import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cipher_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


easy_words = [
    "ПРИВЕТ",
    "СЕКРЕТ",
    "КЛЮЧ",
    "ШИФР",
    "ТАЙНА",
    "ПАРОЛЬ",
    "КОМНАТА",
    "ДЕТЕКТИВ",
    "ЛАБИРИНТ",
    "АРТЕФАКТ"
]

medium_words = [
    "ENIGMA",
    "MATRIX",
    "SHADOW",
    "SECRET",
    "MYSTERY",
    "HACKER",
    "NETWORK",
    "PHANTOM",
    "CIPHER",
    "CONTROL"
]


levels = {
    1: "Шифр наоборот",
    2: "Шифр замены букв символами",
    3: "Каждая вторая буква",
    4: "Цифровой шифр",
    5: "Шифр первая буква",
    6: "Шифр Цезаря",
    7: "Шифр Атбаш",
    8: "Шифр Морзе",
    9: "Шифр Полибия",
    10: "Шифр Гронсфельда",
    11: "Шифр Виженера",
    12: "Шифр Плейфера",
    13: "Шифр четырёх квадратов",
    14: "Шифр Бэкона",
    15: "Шифр Трисемуса",
    16: "Шифр Rail Fence",
    17: "Шифр Колонной перестановки",
    18: "Шифр Вернама",
    19: "Шифр Гамильтона",
    20: "Двойной шифр"
}


cipher_guides = {
    1: {
        "name": "Шифр наоборот",
        "description": """
Простейший шифр.

Суть:
текст просто читается справа налево.

Как расшифровать:
нужно перевернуть строку обратно.

Пример:

ПРИВЕТ → ТЕВИРП

Расшифровка:

ТЕВИРП → ПРИВЕТ

Это не настоящий криптографический шифр,
но отлично подходит для новичков.
"""
    },

    2: {
        "name": "Шифр замены символами",
        "description": """
Буквы заменяются похожими символами.

Примеры:
А → @
О → 0
Е → 3
С → $

Пример:

ПРИВЕТ → ПР183Т

Как расшифровать:
нужно заменить символы обратно на буквы.

Этот метод часто используют:
- хакеры
- никнеймы
- leetspeak
"""
    },

    3: {
        "name": "Каждая вторая буква",
        "description": """
В текст вставляется мусор между буквами.

Пример:

ПРИВЕТ

→ ХПЖРФИЭВЕФТ

Как расшифровать:
читать каждую вторую букву.

П Ж Р И В Е Т
↑ ↑ ↑ ↑ ↑ ↑ ↑

Это шифр сокрытия информации.
"""
    },

    4: {
        "name": "Цифровой шифр",
        "description": """
Каждая буква заменяется номером в алфавите.

А=1
Б=2
В=3

Пример:

ПРИВЕТ

П=17
Р=18
И=10

Результат:

17-18-10-3-6-20

Как расшифровать:
нужно знать таблицу алфавита.
"""
    },

    5: {
        "name": "Шифр первой буквы",
        "description": """
Используются только первые буквы слов.

Пример:

Каждый Охотник Желает Знать Где Сидит Фазан

↓

КОЖЗГСФ

Как расшифровать:
вспомнить исходную фразу.

Часто используется:
- для запоминания
- подсказок
- сокращений
"""
    },

    6: {
        "name": "Шифр Цезаря",
        "description": """
Один из самых известных шифров.

Каждая буква сдвигается по алфавиту.

Сдвиг 3:

А → Г
Б → Д

Пример:

ПРИВЕТ → ТУЛЕИХ

Как расшифровать:
сдвигать буквы обратно.

Шифр использовал Юлий Цезарь.
"""
    },

    7: {
        "name": "Шифр Атбаш",
        "description": """
Алфавит переворачивается.

А ↔ Я
Б ↔ Ю
В ↔ Э

Пример:

ПРИВЕТ → ПОЧЦЪМ

Как расшифровать:
использовать тот же шифр ещё раз.

Атбаш симметричен:
шифрование = расшифровка.
"""
    },

    8: {
        "name": "Шифр Морзе",
        "description": """
Буквы заменяются точками и тире.

А = .-
Б = -...

Пример:

SOS

→ ... --- ...

Как расшифровать:
разделять символы по таблице Морзе.

Использовался:
- телеграфом
- военными
- моряками
"""
    },

    9: {
        "name": "Шифр Полибия",
        "description": """
Буквы превращаются в координаты.

Таблица:

1 2 3 4 5
А Б В Г Д

Пример:

ПРИВЕТ

↓

35 41 24 13 21 43

Как расшифровать:
найти координаты в квадрате.
"""
    },

    10: {
        "name": "Шифр Гронсфельда",
        "description": """
Похож на Цезаря,
но сдвиг постоянно меняется.

Ключ:
312

Сдвиги:
3 1 2 3 1 2 ...

Пример:

HELLO → KFNOP

Как расшифровать:
использовать тот же ключ в обратную сторону.
"""
    },

    11: {
        "name": "Шифр Виженера",
        "description": """
Многоалфавитный шифр.

Используется ключевое слово.

Текст:
ATTACKATDAWN

Ключ:
LEMON

Шифр:
LXFOPVEFRNHR

Каждая буква шифруется
с разным сдвигом.

Как расшифровать:
нужно знать ключ.
"""
    },

    12: {
        "name": "Шифр Плейфера",
        "description": """
Шифрование парами букв.

Создаётся таблица 5×5.

Правила:
- строка → вправо
- столбец → вниз
- прямоугольник → углы

Очень популярен в старой криптографии.
"""
    },

    13: {
        "name": "Шифр четырёх квадратов",
        "description": """
Используются 4 таблицы букв.

Шифрование происходит парами.

Считается усложнённой версией Плейфера.

Требует:
- ключи
- таблицы
- поиск координат
"""
    },

    14: {
        "name": "Шифр Бэкона",
        "description": """
Каждая буква кодируется
5 символами A/B.

A = AAAAA
B = AAAAB

Пример:

HELLO

↓

AABBB AABAA ABABA

Можно скрывать:
- размером букв
- шрифтом
- цветом
"""
    },

    15: {
        "name": "Шифр Трисемуса",
        "description": """
Таблица + постоянный сдвиг.

Каждая следующая буква
сдвигается сильнее.

Очень похож на:
- Виженера
- Цезаря

Но меняет сдвиг автоматически.
"""
    },

    16: {
        "name": "Rail Fence",
        "description": """
Текст записывается зигзагом.

Пример:

WEAREDISCOVERED

Запись:

W . . E . . C
. E . R . D .
. . A . . . .

Как расшифровать:
восстановить зигзаг.
"""
    },

    17: {
        "name": "Колонная перестановка",
        "description": """
Текст записывается в таблицу.

Потом столбцы читаются
в другом порядке.

Используется ключ-перестановка.

Очень популярный тип
перестановочного шифра.
"""
    },

    18: {
        "name": "Шифр Вернама",
        "description": """
Теоретически невзламываемый шифр.

Использует:
- случайный ключ
- XOR

Главное правило:
ключ используется 1 раз.

Если ключ идеален —
взлом невозможен.
"""
    },

    19: {
        "name": "Route Cipher",
        "description": """
Текст записывается в сетку.

Чтение идёт:
- спиралью
- змейкой
- маршрутом

Без знания маршрута
расшифровать сложно.
"""
    },

    20: {
        "name": "Двойной шифр",
        "description": """
Несколько шифров подряд.

Пример:

HELLO
→ Цезарь
→ Атбаш

Чем больше этапов —
тем сложнее взлом.

Очень популярно
в ARG и головоломках.
"""
    }
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        levels=levels
    )


@app.route("/help")
def help_page():
    return render_template(
        "help.html",
        levels=levels,
        cipher_help=cipher_help
    )


@app.route("/play/<int:level>", methods=["GET", "POST"])
@login_required
def play(level):

    result = None
    correct = None
    extra = None

    if request.method == "POST":

        answer = request.form["answer"].upper()
        original_word = request.form["original"].upper()

        if answer == original_word:
            result = "ПРАВИЛЬНО"
        else:
            result = "НЕПРАВИЛЬНО"

        correct = original_word

        return render_template(
            "game.html",
            cipher=request.form["cipher"],
            level_name=levels[level],
            result=result,
            correct=correct,
            level=level,
            extra=request.form.get("extra")
        )

    if level <= 10:
        word = random.choice(easy_words)
    else:
        word = random.choice(medium_words)

    # EASY

    if level == 1:
        cipher_text = easy.reverse_cipher(word)

    elif level == 2:
        cipher_text = easy.symbol_cipher(word)

    elif level == 3:
        cipher_text = easy.second_letter_cipher(word)

    elif level == 4:
        cipher_text = easy.number_cipher(word)

    elif level == 5:
        cipher_text, phrase = easy.first_letter_cipher(word)

        return render_template(
            "game.html",
            cipher=cipher_text,
            level_name=levels[level],
            original=phrase,
            level=level
        )

    elif level == 6:
        shift = random.randint(1, 5)
        cipher_text = easy.caesar_cipher(word, shift)
        extra = f"Сдвиг: {shift}"

    elif level == 7:
        cipher_text = easy.atbash_cipher(word)

    elif level == 8:
        cipher_text = easy.morse_cipher(word)

    elif level == 9:
        cipher_text = easy.polybius_cipher(word)

    elif level == 10:
        cipher_text, key = easy.gronsfeld_cipher(word)
        extra = f"Ключ: {key}"

    # NORMAL

    elif level == 11:
        cipher_text, key = normal.vigenere_cipher(word)
        extra = f"Ключ: {key}"

    elif level == 12:
        cipher_text = normal.playfair_cipher(word)

    elif level == 13:
        cipher_text = normal.four_square_cipher(word)

    elif level == 14:
        cipher_text = normal.bacon_cipher(word)

    elif level == 15:
        cipher_text = normal.trithemius_cipher(word)

    elif level == 16:
        cipher_text = normal.rail_fence_cipher(word)

    elif level == 17:
        cipher_text = normal.column_cipher(word)

    elif level == 18:
        cipher_text = normal.vernam_cipher(word)

    elif level == 19:
        cipher_text = normal.route_cipher(word)

    elif level == 20:
        cipher_text = normal.double_cipher(word)

    else:
        cipher_text = word

    return render_template(
        "game.html",
        cipher=cipher_text,
        level_name=levels[level],
        original=word,
        level=level,
        extra=extra
    )


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':

        response = make_response(redirect('/settings'))

        response.set_cookie(
            'theme',
            request.form.get('theme', 'dark')
        )

        return response

    return render_template('settings.html')


@app.route("/guide")
@login_required
def guide():
    return render_template(
        "guide.html",
        guides=cipher_guides
    )


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_again.data:

            return render_template(
                'register.html',
                form=form,
                message="Пароли не совпадают"
            )

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.login == form.login.data).first():

            return render_template(
                'register.html',
                form=form,
                message="Такой пользователь уже существует"
            )

        user = User(
            login=form.login.data
        )

        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')

    return render_template(
        'register.html',
        form=form
    )


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(
            User.login == form.login.data
        ).first()

        if user and user.check_password(form.password.data):

            login_user(
                user,
                remember=form.remember_me.data
            )

            return redirect("/")

        return render_template(
            'login.html',
            message="Неправильный логин или пароль",
            form=form
        )

    return render_template(
        'login.html',
        form=form
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":

    if not os.path.exists("db"):
        os.mkdir("db")

    db_session.global_init("db/db.sqlite")

    app.run(debug=True)
