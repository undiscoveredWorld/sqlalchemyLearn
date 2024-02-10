import os
import time

from config import DB_USER, DB_PASS, DB_NAME, DOCKER_MODE


def start_postgres():
    if not DOCKER_MODE:
        os.system(f"docker run -d -p 5431:5432 --rm \
                    --env POSTGRES_USER={DB_USER} \
                    --env POSTGRES_PASSWORD={DB_PASS} \
                    --env POSTGRES_DB={DB_NAME} \
                    --name=sqlalchemy-test-postgres \
                    postgres:alpine")
        time.sleep(5)


def stop_postgres():
    if not DOCKER_MODE:
        os.system("docker stop sqlalchemy-test-postgres")
