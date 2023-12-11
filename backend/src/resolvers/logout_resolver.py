from fastapi.responses import Response
from src.graphql.__resolve_types import query


# logout resolver
@query.field("logout_user")
async def resolver_logout_user(_root, info):
    request_context = info.context
    res: Response = request_context.response
    user = request_context.user

    # if there is a user
    if user:
        res.delete_cookie("access_token")
        res.delete_cookie("logged_In")
        return True
    else:
        return False
