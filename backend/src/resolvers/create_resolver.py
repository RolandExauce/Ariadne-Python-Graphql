from src.utils.helpers import create_user_logic
from src.graphql.__resolve_types import mutation
from src.utils.types import IUser
from src.utils.errors_and_success_msgs import (
    NOT_AUTHORIZED
)


# create user resolver
@mutation.field("create_user")
async def resolver_create_user(_root, info, create_user_input: IUser):
    request_context = info.context
    auth_rules = request_context.auth_rules
    isAdmin = bool(auth_rules["isAdmin"])
    if not isAdmin:
        return {"custom_error": NOT_AUTHORIZED}
    user_data = {
        "firstname": create_user_input.get("firstname"),
        "lastname": create_user_input.get("lastname"),
        "username": create_user_input.get("username"),
        "role": create_user_input.get("role"),
        "password": create_user_input.get("password"),
        "birthdate": create_user_input.get("birthdate")
    }
    return await create_user_logic(user_data)
