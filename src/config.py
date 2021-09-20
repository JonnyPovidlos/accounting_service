import os

import dotenv

dotenv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

dotenv.load_dotenv(dotenv_file_path)


class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'awesome_secret_key')
