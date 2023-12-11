from src.utils.errors_and_success_msgs import NO_USERS, NO_AUTH
from src.utils.helpers import get_prisma_instance
from src.graphql.__resolve_types import query


# get users resolver
@query.field("get_users")
async def resolver_get_users(_root, info):

    # Retrieve the context and then get the Response object
    request_context = info.context
    auth_rules = request_context.auth_rules
    isAuth = bool(auth_rules["isAuthenticated"])
    if not isAuth:
        return {"custom_error": NO_AUTH}

    # Handle exception appropriately
    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error.get("custom_error")}

    prisma = prisma_instance_or_error
    users = await prisma.user.find_many()

    if users:
        return {
            "users": users
        }
    else:
        return {
            "custom_error": NO_USERS
        }
