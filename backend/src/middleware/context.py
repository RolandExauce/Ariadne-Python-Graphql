from src.middleware.auth import get_authenticated_user
from fastapi.responses import Response
from fastapi.requests import Request
from typing import Dict


class AuthContext:
    def __init__(self, request: Request, response: Response, auth_rules: Dict[str, bool]):
        self.request = request
        self.response = response
        self.auth_rules = auth_rules


# add req, response and user to context
async def get_context_value(req: Request) -> Dict[str, AuthContext]:
    # get user and create a simple rule based on role
    user = await get_authenticated_user(req)
    auth = user is None or isinstance(user, dict) and "custom_error" in user
    is_admin = not auth and user.get("role") == "ADMIN" if user else False
    auth_rules = {
        "isAuthenticated": not auth,
        "isAdmin": is_admin
    }
    return AuthContext(req, Response(), auth_rules)
