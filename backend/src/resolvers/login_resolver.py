from fastapi.responses import Response
from src.utils.load_envs import jwt_access_token_expires_in_hours
from datetime import datetime, timedelta, timezone
from src.graphql.__resolve_types import mutation
from src.utils.login_helper import try_login
from src.utils.types import ILoginInput


# login resolver
@mutation.field("login_user")
async def resolver_login_user(_root, info, login_input: ILoginInput):
    request_context = info.context
    res: Response = request_context.response

    #  login user middleware to retrieve the user
    user_response = await try_login(login_input)
    if all(key in user_response for key in ("user", "access_token")):
        user_data = user_response["user"]
        access_token = user_response["access_token"]

        user_response = {'user': user_data, 'access_token': access_token}
        expires = datetime.utcnow().replace(tzinfo=timezone.utc) + \
            timedelta(hours=jwt_access_token_expires_in_hours)

        # create some cookie options in a dict
        cookie_opts = {
            "expires": expires,
            "secure": True,
            "httponly": True,
            "samesite": "none"
        }

        # use ** to unpack dict and pass it as key value to set_cookie function
        res.set_cookie(key='access_token',
                       value=f'Bearer {access_token}', **cookie_opts)
        res.set_cookie(key="logged_In", value="True", **cookie_opts)

        return user_response
    else:
        custom_error = user_response.get("custom_error")
        return {"custom_error": str(custom_error)}
