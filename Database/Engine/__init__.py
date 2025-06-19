import os
from sqlmodel import create_engine,SQLModel
from dotenv import load_dotenv
from typing import cast

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?sslmode=require"
TESTING_DATABASE_URL = cast(str,os.getenv("TESTING_DATABASE_URL"))

engine = create_engine(url=TESTING_DATABASE_URL,echo=True)