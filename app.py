import os
import random
from faker import Faker

from flask import Flask, render_template, request, redirect, make_response
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from werkzeug.utils import secure_filename

from ciphers import easy, normal
from data import db_session
from data.users import User
from forms.users import RegisterForm, LoginForm
from ciphers.constants import levels, cipher_guides


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




@app.route("/")
def index():
    return render_template(
        "index.html",
        levels=levels
    )


@app.route("/help/<int:level>")
@login_required
def help_page(level=None):
    if level and level in cipher_guides:
        guide = {level: cipher_guides[level]}
        return render_template("help.html", levels=levels, cipher_help=guide, current_level=level)
    return render_template("help.html", levels=levels, cipher_help=cipher_guides, current_level=None)


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
        word = Faker('ru_RU').word().upper()
    else:
        word = Faker('en_US').word().upper()

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
        response.set_cookie('theme', request.form.get('theme', 'dark'), max_age=60*60*24*365)
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

from flask_login import login_user

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    message = None
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()

    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            if user.avatar:
                old_file = os.path.join(app.config['UPLOAD_FOLDER'], user.avatar)
                if os.path.exists(old_file):
                    os.remove(old_file)
                user.avatar = None
                db_sess.commit()
                message = 'Аватар удалён'
            login_user(user, remember=True)  # обновляем сессию
            return render_template('profile.html', user=user, message=message)

        file = request.files.get('avatar')

        if not file or file.filename == '':
            message = 'Файл не выбран'
        elif not allowed_file(file.filename):
            message = 'Разрешены только PNG, JPG, JPEG, GIF'
        else:
            if user.avatar:
                old_file = os.path.join(app.config['UPLOAD_FOLDER'], user.avatar)
                if os.path.exists(old_file):
                    os.remove(old_file)

            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"avatar_{current_user.id}.{ext}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            user.avatar = filename
            db_sess.commit()
            login_user(user, remember=True)  # обновляем сессию
            message = 'Аватар обновлён!'

    return render_template('profile.html', user=user, message=message)

if __name__ == "__main__":

    if not os.path.exists("db"):
        os.mkdir("db")

    db_session.global_init("db/db.sqlite")

    app.run(debug=True)
