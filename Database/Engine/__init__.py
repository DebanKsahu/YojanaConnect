from sqlmodel import create_engine,SQLModel
from Database.ORM_Models.auth_models import *
from Database.ORM_Models.token_models import *
from Database.ORM_Models.criteria_models import *
from Database.ORM_Models.profile_models import *
from Database.ORM_Models.scheme_models import *
from config import settings


USERNAME = settings.USERNAME
PASSWORD = settings.PASSWORD
HOST = settings.HOST
DATABASE_NAME = settings.DATABASE_NAME
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?sslmode=require"
TESTING_DATABASE_URL = settings.TESTING_DATABASE_URL

engine = create_engine(url=DATABASE_URL,echo=True)