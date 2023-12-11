from src.utils.load_envs import ALGORITHM
import jwt


# Sign JWT tokens
def sign_jwt(payload, private_key):
    return jwt.encode(payload=payload, key=private_key, algorithm=ALGORITHM)


# Verify JWT tokens
def verify_jwt(token, public_key):
    try:
        return jwt.decode(jwt=token, key=public_key, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        print(f"Token error: {e}")
    return None
