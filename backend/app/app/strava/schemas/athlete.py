from pydantic import BaseModel


class Athlete(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    # and more
