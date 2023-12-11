from src.utils.errors_and_success_msgs import INVALID_TOKEN
from src.utils.load_envs import JWT_PUBLIC_KEY_ACCESS
from src.utils.helpers import get_prisma_instance
from src.utils.jwt import verify_jwt
from fastapi import Request
import datetime


# authenticate user in request
async def get_authenticated_user(req: Request):
    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error.get("custom_error")}
    prisma = prisma_instance_or_error

    # Check headers (if applicable)
    token = req.headers.get("authorization")
    if token and token.startswith("Bearer"):
        access_token = token.split(" ")[1]
        decoded_user = verify_jwt(access_token, JWT_PUBLIC_KEY_ACCESS)

        if decoded_user:
            try:
                token_expires_in = decoded_user.get("exp")
                expiration_time = datetime.datetime.utcfromtimestamp(
                    token_expires_in)
                current_time = datetime.datetime.utcnow()

                # Check if the token is expired
                if expiration_time > current_time:
                    # Token is not expired, retrieve user from the database
                    found_user = await prisma.user.find_first(
                        where={"id": str(decoded_user.get("user_id"))}
                    )
                    return dict(found_user)
                else:
                    return {"custom_error": "Token has expired"}

            except Exception as e:
                return {"custom_error": f"Login error: {str(e)}"}

    return {"custom_error": INVALID_TOKEN}  # Return error for invalid token
