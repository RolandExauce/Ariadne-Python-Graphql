from src.graphql.__resolve_types import query

# search user resolver 
@query.field("search_user")
def resolver_search_user(_root, info,  username):
    # Your logic to search for a user by username
    # Return either a User or a GraphqlError
    # Example: return user or error

    return "user found"