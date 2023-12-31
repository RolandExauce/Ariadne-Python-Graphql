# from ariadne.asgi.handlers import GraphQLTransportWSHandler
from ariadne.asgi import GraphQL
from ariadne import (
    format_error,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from graphql.error.graphql_error import GraphQLError
from src.utils.load_envs import (
    FRONT_END_APP_URL,
    APP_STATE,
    SERVER_CERT,
    SERVER_KEY,
    GRAPHQL_SCHEMA_PATH,
    DATABASE_PATH
)


# Importing resolver functions
from src.resolvers.delete_resolver import resolver_delete_user
from src.resolvers.update_resolver import resolver_update_user
from src.resolvers.login_resolver import resolver_login_user
from src.resolvers.create_resolver import resolver_create_user
from src.resolvers.get_users_resolver import resolver_get_users
from src.resolvers.search_resolver import resolver_search_user
from src.resolvers.logout_resolver import resolver_logout_user
from src.graphql.__resolve_types import *


# others
from src.middleware.context import get_context_value
from src.utils.helpers import get_prisma_instance
from pathlib import Path
import sqlite3


is_prod = APP_STATE == "production"  # if is prod mode then use ssl certificates

# Defining paths
base_path = Path(__file__).parent
SCHEMA_PATH = base_path / GRAPHQL_SCHEMA_PATH
DB_PATH = base_path / DATABASE_PATH

# Creating FastAPI instance
app = FastAPI(
    title="Bornday App with FastAPI",
    description="Never forget any birthdays again!",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONT_END_APP_URL],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Global variable for database connection
connection: sqlite3.Connection = None


# Format GraphQL errors
def my_format_error(error: GraphQLError, debug: bool = True) -> dict:
    if debug:
        return format_error(error, debug)
    formatted = error.formatted
    formatted["message"] = error.args[0]
    return formatted


# Setting mutation fields
mutation.set_field("login_user", resolver_login_user)
mutation.set_field("create_user", resolver_create_user)
mutation.set_field("update_user", resolver_update_user)
mutation.set_field("delete_user", resolver_delete_user)

# Setting query fields
query.set_field("get_users", resolver_get_users)
query.set_field("search_user", resolver_search_user)
query.set_field("logout_user", resolver_logout_user)

# Loading GraphQL type definitions from .graphql file
type_defs = load_schema_from_path(SCHEMA_PATH)
resolvers = [
    # Resolvers with unions and other resolvers
    get_users_result_union,
    token_response_union,
    create_user_result_union,
    update_user_result_union,
    delete_user_result_union,
    search_user_result_union,
    query,
    mutation
]

# Creating an executable schema with fallback
schema = make_executable_schema(
    type_defs, resolvers, snake_case_fallback_resolvers
)


# On startup, connect to SQLite database
async def startup_event():
    global connection
    try:
        connection = sqlite3.connect(DB_PATH)
        if connection:
            print("Connected to the database successfully!")
    except sqlite3.Error as e:
        print(f"Failed to connect to the database: {e}")
        exit(1)


# When server shuts down
async def shutdown_event():
    prisma_instance_or_error = await get_prisma_instance()
    if connection:
        connection.close()
        await prisma_instance_or_error.disconnect()
        print("DB closed, Prisma Client closed")

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# Create GraphQL App instance
graphql_app = GraphQL(
    schema,
    error_formatter=my_format_error,
    context_value=get_context_value,
    debug=True
)


# Handle POST requests
@app.post("/apiBornDay")
async def handle_graphql_query(req: Request):
    return await graphql_app.handle_request(req)


if __name__ == "__main__":
    import uvicorn
    uvicorn_options = {
        "host": "localhost",
        "port": 5000
    }

    if is_prod:
        uvicorn_options.update({
            "ssl_keyfile": SERVER_KEY,
            "ssl_certfile": SERVER_CERT,
            "host": "dev.server"
        })

    uvicorn.run(app, **uvicorn_options)


# RUN CMD in dev mode: uvicorn src.server:app --reload --host localhost --port 5000

# RUN CMD in prod mode: uvicorn src.server:app --host dev.server --port 5000 --ssl-keyfile path_to_your_server_key/server.key --ssl-certfile path_to_your_server_certificate/server.crt
