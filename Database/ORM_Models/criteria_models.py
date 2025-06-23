from sqlmodel import SQLModel, Field, Relationship

class CriteriaInDB(SQLModel, table=True):
    criteria_id: int = Field(default=None, primary_key=True)
    aadhaar_number: str = Field(foreign_key="userindb.aadhaar_number")
    criteria_name: str
    criteria_value: str
    data_type: str | None = None

class CriteriaExpose(SQLModel):
    criteria_name: str
    criteria_value: str

class CriteriaEdit(SQLModel):
    criteria_name: str | None = None
    criteria_value: str | None = None