from src.utils.load_envs import JWT_PRIVATE_KEY_ACCESS, jwt_access_token_expires_in_hours
from src.utils.errors_and_success_msgs import WRONG_PASSWORD, USER_NOT_FOUND
from src.utils.helpers import get_prisma_instance
from datetime import datetime, timedelta
from src.utils.types import ILoginInput
from src.utils.jwt import sign_jwt
import bcrypt


# login helper middleware
async def try_login(login_params: ILoginInput):
    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error["custom_error"]}

    prisma = prisma_instance_or_error
    try:
        found_user = await prisma.user.find_first(where={"username": str(login_params.get("username"))})

        # if user was found, compare password
        if found_user:
            stored_password = found_user.password
            decrypted_password = bcrypt.checkpw(
                str(login_params.get("password")).encode("utf-8"),
                str(stored_password).encode(
                    "utf-8") if stored_password else "".encode("utf-8")
            )

            # decrypt the password
            if decrypted_password:
                expiration_time = datetime.utcnow() + timedelta(hours=jwt_access_token_expires_in_hours)
                payload = {
                    'user_id': found_user.id,
                    'exp': expiration_time
                }
                access_token = sign_jwt(
                    payload, JWT_PRIVATE_KEY_ACCESS)  # sign token

                return {
                    "user": found_user.model_dump(),
                    "access_token": access_token
                }
            else:
                return {
                    "custom_error": WRONG_PASSWORD
                }
        else:
            return {
                "custom_error": USER_NOT_FOUND
            }
    except Exception as e:
        return {"custom_error": f"Could not log in user: {str(e)}"}
