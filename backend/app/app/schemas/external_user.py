from typing import Optional

from pydantic import BaseModel, EmailStr

import datetime


# Shared properties
class ExternalUserBase(BaseModel):
    external_user_id: str
    external_source: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    external_user_access_token: str = None
    external_user_refresh_token: str = None
    external_user_access_token_expires_at: datetime.datetime = None


# Properties to receive via API on creation
class ExternalUserCreate(ExternalUserBase):
    external_user_id: str
    external_source: str
    full_name: str
    owner_id: int


# Properties to receive via API on update
class ExternalUserUpdate(ExternalUserBase):
    pass


class ExternalUserInDBBase(ExternalUserBase):
    id: int
    external_user_id: str
    external_source: str
    full_name: str
    owner_id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class ExternalUser(ExternalUserInDBBase):
    pass


# Additional properties stored in DB
class ExternalUserInDB(ExternalUserInDBBase):
    pass
