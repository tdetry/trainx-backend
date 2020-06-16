from pydantic import BaseModel
from .athlete import Athlete
from typing import Optional


class Token(BaseModel):
    token_type: str
    expires_at: int
    expires_in: int
    refresh_token: str
    access_token: str
    athlete: Optional[Athlete]
