import os

from dotenv import load_dotenv, dotenv_values

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

ADMIN = int(os.getenv('ADMIN'))

USERS = set()
st_users = dotenv_values().get('USERS').split(',')
for x in st_users:
    a = int(x)
    USERS.add(a)

DB_PATH = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}'
