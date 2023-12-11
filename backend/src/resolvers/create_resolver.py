from src.utils.helpers import create_user_logic
from src.graphql.__resolve_types import mutation
from src.utils.types import IUser
from src.utils.errors_and_success_msgs import NOT_AUTHORIZED


# create user resolver
@mutation.field("create_user")
async def resolver_create_user(_root, info, create_user_input: IUser):

    # access context
    request_context = info.context
    auth_rules = request_context.auth_rules
    is_admin = bool(auth_rules["is_admin"])

    if not is_admin:
        return {"custom_error": NOT_AUTHORIZED}

    # map through dict, assign each key a value
    user_data = {key: create_user_input[key]
                 for key in create_user_input.keys()}
    return await create_user_logic(user_data)
