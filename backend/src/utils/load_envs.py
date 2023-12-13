from dotenv import load_dotenv
from pathlib import Path
import os

base_path = Path(__file__).parent  # parent dir
env_path = (base_path / "../.env")

# Load variables from .env file into the environment
load_dotenv(env_path)

# Access the variables using os.getenv()
JWT_PRIVATE_KEY_ACCESS = str(os.getenv("JWT_PRIVATE_KEY_ACCESS"))
JWT_PUBLIC_KEY_ACCESS = str(os.getenv("JWT_PUBLIC_KEY_ACCESS"))
ALGORITHM = str(os.getenv("ALGORITHM"))
jwtAccessTokenExpiresIn = str(os.getenv("jwtAccessTokenExpiresIn"))
jwt_access_token_expires_in_hours = float(jwtAccessTokenExpiresIn)


FRONT_END_APP_URL = str(os.getenv("FRONT_END_APP_URL"))
GRAPHQL_SCHEMA_PATH = str(os.getenv("GRAPHQL_SCHEMA_PATH"))
DATABASE_PATH = str(os.getenv("DATABASE_PATH"))

SERVER_CERT = str(os.getenv("SERVER_CERT"))
SERVER_KEY = str(os.getenv("SERVER_KEY"))
APP_STATE = str(os.getenv("APP_STATE"))
