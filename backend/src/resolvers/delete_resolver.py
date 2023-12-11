from src.graphql.__resolve_types import mutation
from src.utils.errors_and_success_msgs import NOT_AUTHORIZED

# delte user resolver
@mutation.field("delete_user")
def resolver_delete_user(_root, info, id):

    # Retrieve the context and then get the Response object
    request_context = info.context
    user = request_context.user
    user_role = user.get("role")

    # Check if the user is an admin; if not, return an error
    if user is not None and user_role != "ADMIN":
        return {"custom_error": NOT_AUTHORIZED}


    # Your logic to delete a user
    # Return either a User or a GraphqlError
    # Example: return deleted_user or error

    return "user was deleted"