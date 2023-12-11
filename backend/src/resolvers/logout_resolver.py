from src.graphql.__resolve_types import query

# logout resolver 
@query.field("logout_user")
def resolver_logout_user(_root, info, ):
    #Your logout logic
    #Return True if successful

    return True