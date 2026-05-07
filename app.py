from flask import Flask, render_template, request
import random

app = Flask(__name__)

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
    5: "Шифр первая буква"
}


# 1 Переворот
def reverse_cipher(text):
    return text[::-1]


# 2 Символы
def symbol_cipher(text):

    symbols = {
        "А": "@",
        "Б": "6",
        "В": "8",
        "Е": "3",
        "И": "1",
        "О": "0",
        "С": "$",
        "Т": "7"
    }

    result = ""

    for letter in text:
        result += symbols.get(letter, letter)

    return result


# 3 Каждая секунда
def second_letter_cipher(text):

    garbage = "ХЖФЭQW"

    result = ""

    for letter in text:
        result += random.choice(garbage)
        result += letter

    return result


# 4 Номера
def number_cipher(text):

    alphabet = {
        "А": 1, "Б": 2, "В": 3,
        "Г": 4, "Д": 5, "Е": 6,
        "Ж": 7, "З": 8, "И": 9,
        "Й": 10, "К": 11, "Л": 12,
        "М": 13, "Н": 14, "О": 15,
        "П": 16, "Р": 17, "С": 18,
        "Т": 19, "У": 20, "Ф": 21,
        "Х": 22, "Ц": 23, "Ч": 24,
        "Ш": 25, "Щ": 26, "Ъ": 27,
        "Ы": 28, "Ь": 29, "Э": 30,
        "Ю": 31, "Я": 32
    }

    result = []

    for letter in text:
        if letter in alphabet:
            result.append(str(alphabet[letter]))

    return "-".join(result)


# 5 Первое письмо
def first_letter_cipher(text):

    phrases = [
        ("Каждый Охотник Желает Знать Где Сидит Фазан", "КОЖЗГСФ"),
        ("Мама Мыла Раму", "ММР"),
        ("Старый Дом Очень Тёмный", "СДОТ")
    ]

    phrase = random.choice(phrases)

    return phrase[1], phrase[0]


@app.route("/")
def index():

    return render_template(
        "index.html",
        levels=levels
    )


@app.route("/play/<int:level>", methods=["GET", "POST"])
def play(level):

    result = None
    correct = None

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

        return render_template(
            "game.html",
            cipher=cipher_text,
            level_name=levels[level],
            result=result,
            correct=correct,
            original=original_word,
            level=level
        )

    # GET
    word = random.choice(words)

    if level == 1:
        cipher_text = reverse_cipher(word)

    elif level == 2:
        cipher_text = symbol_cipher(word)

    elif level == 3:
        cipher_text = second_letter_cipher(word)

    elif level == 4:
        cipher_text = number_cipher(word)

    elif level == 5:

        cipher_text, phrase = first_letter_cipher(word)

        return render_template(
            "game.html",
            cipher=cipher_text,
            level_name=levels[level],
            original=phrase,
            level=level
        )

    else:
        cipher_text = reverse_cipher(word)

    return render_template(
        "game.html",
        cipher=cipher_text,
        level_name=levels[level],
        original=word,
        level=level
    )


if __name__ == "__main__":
    app.run(debug=True)