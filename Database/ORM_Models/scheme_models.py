from sqlmodel import SQLModel, Field
from datetime import date

class SchemeInDB(SQLModel,table=True):
    scheme_id: int = Field(default=None, primary_key=True)
    scheme_name: str
    sector: str
    scheme_type: str
    launch_date: date
    is_active: bool
    website: str

class SchemeExpose(SQLModel):
    scheme_id: int
    scheme_name: str
    sector: str
    scheme_type: str
    launch_date: date
    is_active: bool
    website: str
    match_score: float