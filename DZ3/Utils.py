import hashlib

def hash_password(password_for_hash):
    "Переводит пароль в hash"
    password_bytes = password_for_hash.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


def check_date(date_for_check):
    try:
        if (len(date_for_check) == 10 and isinstance(int(date_for_check[0:4]), int) and date_for_check[4] == '-'
                and date_for_check[7] == '-' and isinstance(int(date_for_check[5:7]), int)
                and isinstance(int(date_for_check[8:10]), int)):
            return True
    except:
        return False
