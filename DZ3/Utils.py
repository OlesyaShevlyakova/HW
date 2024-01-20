import hashlib

def hash_password(password_for_hash):
    "Переводит пароль в hash"
    password_bytes = password_for_hash.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()