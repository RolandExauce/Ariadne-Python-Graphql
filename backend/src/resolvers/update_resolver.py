from src.graphql.__resolve_types import mutation

# update user resolver 
@mutation.field("update_user")
def resolver_update_user(_root, info, id):
    # Your logic to update a user
    # Return either a User or a GraphqlError
    # Example: return updated_user or error

    return "user updated"