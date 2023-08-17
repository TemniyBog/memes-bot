import os
from dotenv import load_dotenv

load_dotenv()

PGHOST = str(os.getenv('PGHOST'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
PGDATABASE = str(os.getenv('PGDATABASE'))
PGUSER = str(os.getenv('PGUSER'))
PGPORT = str(os.getenv('PGPORT'))

REDIS_HOST = str(os.getenv('REDIS_HOST'))
REDIS_PORT = str(os.getenv('REDIS_PORT'))
REDIS_DB = str(os.getenv('REDIS_DB'))
REDIS_PASSWORD = str(os.getenv('REDIS_PASSWORD'))

TOKEN = str(os.getenv('TOKEN'))

DB_PATH = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'