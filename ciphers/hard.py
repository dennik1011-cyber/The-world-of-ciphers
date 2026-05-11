import random

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 16. Rail Fence
def rail_fence_cipher(text, rails=3):
    fence = [[] for _ in range(rails)]

    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)

        rail += direction

        if rail == rails - 1:
            direction = -1
        elif rail == 0:
            direction = 1

    return "".join("".join(row) for row in fence)


# 17. Колонная перестановка
def column_cipher(text):
    cols = 4

    while len(text) % cols != 0:
        text += "X"

    rows = [text[i:i + cols] for i in range(0, len(text), cols)]

    order = [1, 3, 0, 2]

    result = ""

    for col in order:
        for row in rows:
            result += row[col]

    return result


# 18. Вернам
def vernam_cipher(text):
    key = ''.join(random.choice(ALPHABET) for _ in range(len(text)))

    result = ""

    for t, k in zip(text.upper(), key):
        if t in ALPHABET:
            result += ALPHABET[
                (ALPHABET.index(t) ^ ALPHABET.index(k)) % 26
            ]
        else:
            result += t

    return result, key


# 19. Гамильтон
def route_cipher(text):
    size = 4

    while len(text) < size * size:
        text += "X"

    matrix = []

    idx = 0

    for _ in range(size):
        row = []

        for _ in range(size):
            row.append(text[idx])
            idx += 1

        matrix.append(row)

    result = ""

    top = 0
    bottom = size - 1
    left = 0
    right = size - 1

    while top <= bottom and left <= right:

        for i in range(left, right + 1):
            result += matrix[top][i]

        top += 1

        for i in range(top, bottom + 1):
            result += matrix[i][right]

        right -= 1

        if top <= bottom:
            for i in range(right, left - 1, -1):
                result += matrix[bottom][i]

            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                result += matrix[i][left]

            left += 1

    return result


# 20. Двойной
def double_cipher(text):
    shifted = ""

    for char in text.upper():
        if char in ALPHABET:
            idx = (ALPHABET.index(char) + 3) % 26
            shifted += ALPHABET[idx]
        else:
            shifted += char

    reversed_alphabet = ALPHABET[::-1]

    result = ""

    for char in shifted:
        if char in ALPHABET:
            result += reversed_alphabet[ALPHABET.index(char)]
        else:
            result += char

    return result