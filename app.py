import os

from flask import Flask, render_template, request, redirect, make_response
import random

from flask_login import login_user, login_required, logout_user, LoginManager

from ciphers import easy
from data import db_session
from data.users import User
from forms.users import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

words = [
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
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        levels=levels
    )


@app.route("/play/<int:level>", methods=["GET", "POST"])
@login_required
def play(level):
    result = None
    correct = None
    extra = None  # Для ключа Гронсфельда или фразы

    # POST
    if request.method == "POST":

        answer = request.form["answer"].upper()
        original_word = request.form["original"]

        if answer == original_word:
            result = "ПРАВИЛЬНО"
        else:
            result = "НЕПРАВИЛЬНО"

        correct = original_word
        cipher_text = request.form["cipher"]
        extra = request.form.get("extra", "")

        return render_template(
            "game.html",
            cipher=cipher_text,
            level_name=levels[level],
            result=result,
            correct=correct,
            original=original_word,
            level=level,
            extra=extra,
        )

    # GET
    word = random.choice(words)

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
            level=level,
        )

    elif level == 6:
        shift = random.randint(1, 33)
        cipher_text = easy.caesar_cipher(word, shift)
        extra = str(shift)

    elif level == 7:
        cipher_text = easy.atbash_cipher(word)

    elif level == 8:
        cipher_text = easy.morse_cipher(word)

    elif level == 9:
        cipher_text = easy.polybius_cipher(word)

    elif level == 10:
        cipher_text, key = easy.gronsfeld_cipher(word)
        extra = key

    else:
        cipher_text = easy.reverse_cipher(word)

    return render_template(
        "game.html",
        cipher=cipher_text,
        level_name=levels[level],
        original=word,
        level=level,
        extra=extra,
    )


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        music = request.form.get('music', 'off')
        volume = request.form.get('volume', '75')
        theme = request.form.get('theme', 'hacker')
        animations = request.form.get('animations', 'off')
        language = request.form.get('language', 'ru')

        response = make_response(redirect('/settings?saved=1'))
        response.set_cookie('music', music, max_age=60 * 60 * 24 * 365)
        response.set_cookie('volume', volume, max_age=60 * 60 * 24 * 365)
        response.set_cookie('theme', theme, max_age=60 * 60 * 24 * 365)
        response.set_cookie('animations', animations, max_age=60 * 60 * 24 * 365)
        response.set_cookie('language', language, max_age=60 * 60 * 24 * 365)
        return response

    return render_template('settings.html')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("db/db.sqlite")
    app.run(debug=True)
