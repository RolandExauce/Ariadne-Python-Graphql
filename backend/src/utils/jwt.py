from src.utils.load_envs import ALGORITHM
import jwt


# sign jwt tokens
def sign_jwt(payload, private_key):
    return jwt.encode(payload=payload, key=private_key, algorithm=ALGORITHM)


# verify jwt tokens
def verify_jwt(token, public_key):
    try:
        return jwt.decode(jwt=token, key=public_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
    return None
