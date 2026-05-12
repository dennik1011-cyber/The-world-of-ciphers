import random

LOWER = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н",
         "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
UPPER = [i.upper() for i in LOWER]


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
