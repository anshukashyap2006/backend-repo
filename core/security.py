from passlib.context import CryptContext

# creating a hash context with bcrypt and deprecated= "auto" so that in future if bcrypt becomes obsolete, hashing upgrades automatically
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password: str) -> str:
    try:
       return pwd_context.hash(password)
    except Exception as e:
        print("Unable to hash password")
        raise e

def verify_password(plain_password:str,hashed_password:str)-> bool:
    return pwd_context.verify(plain_password,hashed_password)





