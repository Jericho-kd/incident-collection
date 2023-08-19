from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST: str | None = os.environ.get("DB_HOST")
DB_PORT: str | None = os.environ.get("DB_PORT")
DB_NAME: str | None = os.environ.get("DB_NAME")
# DB_USER: str | None = os.environ.get("DB_USER")
# DB_PASS: str | None = os.environ.get("DB_PASS")