from ariadne import MutationType, QueryType, UnionType

# Define resolvers
query = QueryType()
mutation = MutationType()

# all unions
token_response_union = UnionType("TokenResponse")
create_user_result_union = UnionType("CreateUserResult")
update_user_result_union = UnionType("UpdateUserResult")
delete_user_result_union = UnionType("DeleteUserResult")
search_user_result_union = UnionType("SearchUserResult")
get_users_result_union = UnionType("GetUsersResult")


# resolvers for union object types #######################################
@get_users_result_union.type_resolver
def resolve_get_users_response_type(obj, *_):
    if "users" in obj:
        return "UsersSuccess"
    else:
        return "GraphqlError"


@token_response_union.type_resolver
def resolve_token_response_type(obj, *_):
    if "user" in obj:
        return "UserResponse"
    else:
        return "GraphqlError"


@create_user_result_union.type_resolver
def resolve_create_user_result_type(obj, *_):
    if "message" in obj:
        return "Success"
    else:
        return "GraphqlError"


@update_user_result_union.type_resolver
def resolve_update_user_result_type(obj, *_):
    if "message" in obj:
        return "Success"
    else:
        return "GraphqlError"


@delete_user_result_union.type_resolver
def resolve_delete_user_result_type(obj, *_):
    if "message" in obj:
        return "Success"
    else:
        return "GraphqlError"


# here 'cause we returning a User Type, we need to check
# if one of the User fields is on obj, e.g "id" field
@search_user_result_union.type_resolver
def resolve_search_user_result_type(obj, *_):
    if "id" in obj:
        return "User"
    else:
        return "GraphqlError"
