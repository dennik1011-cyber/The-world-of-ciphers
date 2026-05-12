ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# 11. Виженер
def vigenere_cipher(text, key="KEY"):
    text = text.upper()
    key = key.upper()

    result = ""
    key_index = 0

    for char in text:
        if char in ALPHABET:
            t = ALPHABET.index(char)
            k = ALPHABET.index(key[key_index % len(key)])

            result += ALPHABET[(t + k) % 26]
            key_index += 1
        else:
            result += char

    return result, key


# 12. Плейфер
def playfair_cipher(text, key="CIPHER"):
    text = text.upper().replace("J", "I")
    key = key.upper().replace("J", "I")

    table = []
    used = set()

    for char in key:
        if char in ALPHABET and char not in used:
            table.append(char)
            used.add(char)

    for char in ALPHABET:
        if char not in used:
            table.append(char)

    matrix = [table[i:i + 5] for i in range(0, 25, 5)]

    clean = "".join(c for c in text if c in ALPHABET)

    if len(clean) % 2 != 0:
        clean += "X"

    pairs = []
    i = 0
    while i < len(clean):
        if i == len(clean) - 1:
            pairs.append(clean[i] + "X")
            i += 1
        elif clean[i] == clean[i + 1]:
            pairs.append(clean[i] + "X")
            i += 1
        else:
            pairs.append(clean[i] + clean[i + 1])
            i += 2

    def find_pos(char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return 0, 0

    result = ""
    for a, b in pairs:
        r1, c1 = find_pos(a)
        r2, c2 = find_pos(b)

        if r1 == r2:
            result += matrix[r1][(c1 + 1) % 5]
            result += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 + 1) % 5][c1]
            result += matrix[(r2 + 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result


# 13. Четыре квадрата
def four_square_cipher(text, key1="CIPHER", key2="SECRET"):
    text = text.upper().replace("J", "I")
    key1 = key1.upper().replace("J", "I")
    key2 = key2.upper().replace("J", "I")

    square1 = [list(ALPHABET[i:i + 5]) for i in range(0, 25, 5)]
    square4 = [list(ALPHABET[i:i + 5]) for i in range(0, 25, 5)]

    t2 = []
    used2 = set()
    for c in key1:
        if c in ALPHABET and c not in used2:
            t2.append(c)
            used2.add(c)
    for c in ALPHABET:
        if c not in used2:
            t2.append(c)
    square2 = [t2[i:i + 5] for i in range(0, 25, 5)]

    t3 = []
    used3 = set()
    for c in key2:
        if c in ALPHABET and c not in used3:
            t3.append(c)
            used3.add(c)
    for c in ALPHABET:
        if c not in used3:
            t3.append(c)
    square3 = [t3[i:i + 5] for i in range(0, 25, 5)]

    clean = "".join(c for c in text if c in ALPHABET)
    if len(clean) % 2 != 0:
        clean += "X"

    pairs = []
    i = 0
    while i < len(clean):
        if i == len(clean) - 1:
            pairs.append(clean[i] + "X")
            i += 1
        elif clean[i] == clean[i + 1]:
            pairs.append(clean[i] + "X")
            i += 1
        else:
            pairs.append(clean[i] + clean[i + 1])
            i += 2

    def find_in(sq, char):
        for r in range(5):
            for c in range(5):
                if sq[r][c] == char:
                    return r, c
        return 0, 0

    result = ""
    for a, b in pairs:
        r1, c1 = find_in(square1, a)
        r4, c4 = find_in(square4, b)

        result += square2[r1][c4]
        result += square3[r4][c1]

    return result


# 14. Бэкон
def bacon_cipher(text):
    bacon = {
        "A": "AAAAA",
        "B": "AAAAB",
        "C": "AAABA",
        "D": "AAABB",
        "E": "AABAA",
        "F": "AABAB",
        "G": "AABBA",
        "H": "AABBB",
        "I": "ABAAA",
        "J": "ABAAB",
        "K": "ABABA",
        "L": "ABABB",
        "M": "ABBAA",
        "N": "ABBAB",
        "O": "ABBBA",
        "P": "ABBBB",
        "Q": "BAAAA",
        "R": "BAAAB",
        "S": "BAABA",
        "T": "BAABB",
        "U": "BABAA",
        "V": "BABAB",
        "W": "BABBA",
        "X": "BABBB",
        "Y": "BBAAA",
        "Z": "BBAAB",
    }

    result = []

    for char in text.upper():
        if char in bacon:
            result.append(bacon[char])

    return " ".join(result)


# 15. Трисемус
def trithemius_cipher(text):
    result = ""

    for i, char in enumerate(text.upper()):
        if char in ALPHABET:
            idx = ALPHABET.index(char)
            result += ALPHABET[(idx + i) % 26]
        else:
            result += char

    return result
