from src.graphql.__resolve_types import mutation
from src.utils.errors_and_success_msgs import NOT_AUTHORIZED, user_op_msgs
from src.utils.helpers import get_prisma_instance


# delete user resolver
@mutation.field("delete_user")
async def resolver_delete_user(_root, info, id):

    # get context
    request_context = info.context
    auth_rules = request_context.auth_rules
    is_admin = bool(auth_rules.get("is_admin", False))

    if not is_admin:
        return {"custom_error": NOT_AUTHORIZED}

    # prisma instance
    prisma_instance_or_error = await get_prisma_instance()
    if isinstance(prisma_instance_or_error, dict) and "custom_error" in prisma_instance_or_error:
        return {"custom_error": prisma_instance_or_error["custom_error"]}
    prisma = prisma_instance_or_error

    try:
        # similar to js, returning by checking similar to a ternary operator
        deleted_user = await prisma.user.delete(where={"id": id})
        return {"message": user_op_msgs(op="DELETE")} if deleted_user else {"custom_error": user_op_msgs(op="DELETE", caseErr="FAILED")}
    except Exception as e:
        return {"custom_error": str(e)}
