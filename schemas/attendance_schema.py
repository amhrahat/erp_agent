from frappeclient import frappeclient

from pydantic import BaseModel, Field
from typing import Optional, Literal


class AttendanceQueryInput(BaseModel):
    employee: Optional[str] = Field(None, description="Employee ID or name")
    status: Optional[Literal["Present", "Absent", "On Leave"]] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    limit: int = 20