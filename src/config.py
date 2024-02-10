from os import environ
from dotenv import load_dotenv

load_dotenv()

DOCKER_MODE = environ.get("DOCKER_MODE") or False

DB_USER = environ["DB_USER"]
DB_PASS = environ["DB_PASS"]
DB_NAME = environ["DB_NAME"]

if not DOCKER_MODE:
    URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@127.0.0.1:5431/{DB_NAME}"
else:
    DB_HOST = environ["DB_HOST"]
    URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
