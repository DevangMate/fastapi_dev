from pwdlib import PasswordHash

# This automatically configures Argon2 as the hashing algorithm
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

# You will need this function later in the course for the login route!
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)