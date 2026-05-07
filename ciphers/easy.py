import random

LOWER = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н",
         "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
UPPER = [i.upper() for i in LOWER]


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


# 6 Цезарь
def caesar_cipher(text, shift=3):
    result = ""

    for letter in text:
        if letter in LOWER:
            idx = LOWER.index(letter) + shift
            while idx >= len(LOWER):
                idx -= len(LOWER)
            while idx < 0:
                idx += len(LOWER)
            result += LOWER[idx]
        elif letter in UPPER:
            idx = UPPER.index(letter) + shift
            while idx >= len(UPPER):
                idx -= len(UPPER)
            while idx < 0:
                idx += len(UPPER)
            result += UPPER[idx]
        else:
            result += letter

    return result


# 7 Атбаш
def atbash_cipher(text):
    REV_LOWER = LOWER[::-1]
    REV_UPPER = UPPER[::-1]

    result = ""

    for letter in text:
        if letter in LOWER:
            result += REV_LOWER[LOWER.index(letter)]
        elif letter in UPPER:
            result += REV_UPPER[UPPER.index(letter)]
        else:
            result += letter

    return result


# 8 Морзе
def morse_cipher(text):
    morse = {
        "А": ".-", "Б": "-...", "В": ".--", "Г": "--.", "Д": "-..",
        "Е": ".", "Ж": "...-", "З": "--..", "И": "..", "Й": ".---",
        "К": "-.-", "Л": ".-..", "М": "--", "Н": "-.", "О": "---",
        "П": ".--.", "Р": ".-.", "С": "...", "Т": "-", "У": "..-",
        "Ф": "..-.", "Х": "....", "Ц": "-.-.", "Ч": "---.", "Ш": "----",
        "Щ": "--.-", "Ъ": "--.--", "Ы": "-.--", "Ь": "-..-", "Э": "..-..",
        "Ю": "..--", "Я": ".-.-",
    }

    result = []

    for letter in text.upper():
        if letter == " ":
            result.append("/")
        elif letter in morse:
            result.append(morse[letter])
        else:
            result.append(letter)

    return " ".join(result)


# 9 Полибий
def polybius_cipher(text):
    result = []

    for letter in text:
        if letter in LOWER:
            idx = LOWER.index(letter)
            row = idx // 6 + 1
            col = idx % 6 + 1
            result.append(str(row) + str(col))
        elif letter in UPPER:
            idx = UPPER.index(letter)
            row = idx // 6 + 1
            col = idx % 6 + 1
            result.append(str(row) + str(col))
        else:
            result.append(letter)

    return " ".join(result)


# 10 Гронсфельд
def gronsfeld_cipher(text, key=None):
    if key is None:
        key = str(random.randint(100, 999))

    digits = [int(d) for d in key]

    result = ""
    key_idx = 0

    for letter in text:
        shift = digits[key_idx % len(digits)]

        if letter in LOWER:
            idx = LOWER.index(letter) + shift
            while idx >= len(LOWER):
                idx -= len(LOWER)
            result += LOWER[idx]
            key_idx += 1
        elif letter in UPPER:
            idx = UPPER.index(letter) + shift
            while idx >= len(UPPER):
                idx -= len(UPPER)
            result += UPPER[idx]
            key_idx += 1
        else:
            result += letter

    return result, key
