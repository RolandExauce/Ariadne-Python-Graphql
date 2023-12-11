from src.utils.errors_and_success_msgs import NO_USERS, NO_AUTH
from src.utils.helpers import get_prisma_instance
from src.graphql.__resolve_types import query


# get users resolver
@query.field("get_users")
async def resolver_get_users(_root, info):
    request_context = info.context
    auth_rules = request_context.auth_rules
    is_auth = bool(auth_rules.get("is_authenticated", False))
    is_admin = bool(auth_rules.get("is_admin", False))

    if not is_auth:
        return {"custom_error": NO_AUTH}

    # get prisma err or instance
    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error["custom_error"]}
    prisma = prisma_instance_or_error

    users = await prisma.user.find_many()

    if users:
        if is_admin:
            return {"users": users}
        else:
            modified_users = [user.model_dump(
                exclude={"id"}) for user in users]
            return {"users": modified_users}
    else:
        return {"custom_error": NO_USERS}
