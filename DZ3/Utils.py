import hashlib
from datetime import datetime

def hash_password(password_for_hash):
    "Переводит пароль в hash"
    password_bytes = password_for_hash.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


def check_date(date_for_check):
    "Проверяет, что дата введена в формате YYYY-MM-DD, например, 2023-01-05"
    try:
        if (len(date_for_check) == 10 and isinstance(int(date_for_check[0:4]), int) and date_for_check[4] == '-'
                and date_for_check[7] == '-' and isinstance(int(date_for_check[5:7]), int)
                and isinstance(int(date_for_check[8:10]), int)):
            return True
    except:
        return False

def str_to_date(str_data):
    "Перевод даты из типа str в тип data"
    year = int(str_data[0:4])
    month = int(str_data[5:7])
    day = int(str_data[8:10])
    data_data = datetime(year, month, day)
    return data_data

