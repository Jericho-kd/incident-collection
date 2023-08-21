import dotenv
from pathlib import Path


config_path = Path(__file__).resolve().parents[1]
config_env = dotenv.dotenv_values(config_path / 'config.env')

DB_HOST = config_env.get('DB_HOST')
DB_PORT = config_env.get('DB_PORT')
DB_NAME = config_env.get('DB_NAME')