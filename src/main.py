from fastapi import FastAPI
from common.db.postgres import start_postgres, stop_postgres

app = FastAPI()

app.add_event_handler("startup", start_postgres)
app.add_event_handler("shutdown", stop_postgres)
