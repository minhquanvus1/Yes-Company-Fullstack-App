import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

TEST_DB_USERNAME = os.getenv('TEST_DB_USERNAME')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
TEST_DB_HOST = os.getenv('TEST_DB_HOST')
TEST_DB_PORT = os.getenv('TEST_DB_PORT')
TEST_DB_NAME = os.getenv('TEST_DB_NAME')

if not os.getenv('DATABASE_URL'):
    database_path = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
else:
    database_path = os.getenv('DATABASE_URL')
    if database_path.startswith("postgres://"):
        database_path = database_path.replace("postgres://", "postgresql://", 1)
        
production_config = {
    "SQLALCHEMY_DATABASE_URI": database_path,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}

test_config = {
    "SQLALCHEMY_DATABASE_URI": f'postgresql://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}',
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}