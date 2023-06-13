import random

CYRILLIC_FIRST_LETTER_CODE = ord('а')
CYRILLIC_LAST_LETTER_CODE = ord('я')


def get_random_int(length):
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


def get_random_str_ru(length):
    return "".join([chr(random.randint(CYRILLIC_FIRST_LETTER_CODE, CYRILLIC_LAST_LETTER_CODE)) for _ in range(length)])
