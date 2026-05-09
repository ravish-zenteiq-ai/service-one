from pwdlib import PasswordHash

pass_hash = PasswordHash.recommended()

def create_hash(password: str) -> str:
    return pass_hash.hash(password)

def verify_hash(password, hashed) -> bool:
    return pass_hash.verify(password, hashed)


    