import hashlib
def hashing(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

