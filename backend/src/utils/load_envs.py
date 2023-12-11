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
