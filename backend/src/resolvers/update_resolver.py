from src.utils.helpers import get_prisma_instance
from src.graphql.__resolve_types import mutation
from src.utils.errors_and_success_msgs import (
    NOT_AUTHORIZED, USER_NOT_FOUND,
    NO_VALUES_UPDATED, user_op_msgs
)


# update user resolver
@mutation.field("update_user")
async def resolver_update_user(_root, info, id, update_user_input):
    # Retrieve the context and then get the Response object
    request_context = info.context
    auth_rules = request_context.auth_rules
    is_admin = bool(auth_rules["is_admin"])

    mod_update_data = {
        "firstname": update_user_input.get("new_firstname"),
        "lastname": update_user_input.get("new_lastname"),
        "username": update_user_input.get("new_username"),
        "password": update_user_input.get("new_password"),
        "role": update_user_input.get("new_role"),
        "birthdate": update_user_input.get("new_birthdate")
    }

    # Filter out None values from mod_update_data
    mod_update_data = {key: value for key,
                       value in mod_update_data.items() if value is not None}

    # Check if the user is authorized to update
    if not is_admin:
        return {"custom_error": NOT_AUTHORIZED}

    # Get Prisma instance
    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error.get("custom_error")}
    prisma = prisma_instance_or_error

    # Find the user by ID
    user = await prisma.user.find_unique(where={"id": id})
    if not user:
        return {"custom_error": USER_NOT_FOUND}

    # Check if the input data is the same as the existing user data
    if all(getattr(user, field) == value for field, value in mod_update_data.items()):
        return {"custom_error": NO_VALUES_UPDATED}

    try:
        # Update user data with non-None values only
        updated_user = await prisma.user.update(where={"id": id}, data=mod_update_data)
        return {"message": user_op_msgs(op="UPDATE")} if updated_user else {
            "custom_error": user_op_msgs(op="UPDATE", caseErr="FAILED")
        }
    except Exception as e:
        return {"custom_error": str(e)}
