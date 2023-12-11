from src.utils.load_envs import jwt_access_token_expires_in_hours
from datetime import datetime, timedelta, timezone
from src.graphql.__resolve_types import mutation
from src.utils.login_helper import try_login
from src.utils.types import ILoginInput


# login resolver
@mutation.field("login_user")
async def resolver_login_user(_root, info, login_input: ILoginInput):

    # Retrieve the context and then get the Response object
    request_context = info.context
    res = request_context.response

    # pass login input to login helper middleware
    user_response = await try_login(login_input)
    if "user" in user_response and "access_token" in user_response:
        user_data = user_response.get("user")
        access_token = user_response.get("access_token")

        # Construct response content
        user_response = {
            'user': user_data,
            'access_token': access_token,
        }

        # expiration time for cookies
        expires = datetime.utcnow().replace(tzinfo=timezone.utc) + \
            timedelta(hours=jwt_access_token_expires_in_hours)

        # Set the cookies in the response headers
        res.set_cookie(
            key='access_token',
            value=f'Bearer {access_token}',
            expires=expires,
            secure=True,
            httponly=True,
            samesite="none"
        )
        res.set_cookie(
            key="logged_In",
            value="True",
            expires=expires,
            secure=True,
            httponly=True,
            samesite="none"
        )

        return user_response
    else:
        custom_error = user_response.get("custom_error")
        return {"custom_error": str(custom_error)}
