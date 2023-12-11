from src.graphql.__resolve_types import query
from src.utils.errors_and_success_msgs import NO_AUTH, USER_NOT_FOUND
from src.utils.helpers import get_prisma_instance


# search user resolver
@query.field("search_user")
async def resolver_search_user(_root, info, username):
    request_context = info.context
    auth_rules = request_context.auth_rules
    is_auth = bool(auth_rules.get("is_authenticated", False))

    if not is_auth:
        return {"custom_error": NO_AUTH}

    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error.get("custom_error")}

    prisma = prisma_instance_or_error
    user = await prisma.user.find_first(where={"username": str(username)})

    # return entire user dict or err msg
    if user:
        return dict(user)
    else:
        return {"custom_error": USER_NOT_FOUND}
