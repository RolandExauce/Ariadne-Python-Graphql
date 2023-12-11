from src.middleware.auth import get_authenticated_user
from fastapi.responses import Response
from fastapi.requests import Request
from typing import Dict
from src.utils.types import IUser


class AuthContext:
    def __init__(self, request: Request, response: Response, auth_rules: Dict[str, bool], user: IUser):
        self.request = request
        self.response = response
        self.auth_rules = auth_rules
        self.user = user


# add req, response and user to context
async def get_context_value(req: Request) -> Dict[str, AuthContext]:
    # Get user and create a simple rule based on role
    user = await get_authenticated_user(req)
    
    # Check if user is authenticated and determine admin status
    auth = user is None or isinstance(user, dict) and "custom_error" in user
    is_admin = not auth and user.get("role") == "ADMIN" if user else False
    
    # Define authentication rules
    auth_rules = {
        "is_authenticated": not auth,
        "is_admin": is_admin
    }
    
    # Create and return AuthContext object
    return AuthContext(req, Response(), auth_rules, user)
