from faker import Faker

# Английский
fake_en = Faker('en_US')
print(fake_en.word())

# Русский
fake_ru = Faker('ru_RU')
print(fake_ru.word().upper())

