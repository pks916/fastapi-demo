from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["sha256_crypt"])


def hash_func(password:str):
    return pwd_context.hash(password)

def verify_func(hashed_password:str, plain_password:str):
    return pwd_context.verify(plain_password, hashed_password)
    # return pwd_context.hash(plain_password) == hashed_password
