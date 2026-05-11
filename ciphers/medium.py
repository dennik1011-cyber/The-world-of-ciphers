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
def playfair_cipher(text):
    return f"PLAYFAIR-{text}"


# 13. Четыре квадрата
def four_square_cipher(text):
    return f"FOURSQUARE-{text}"


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