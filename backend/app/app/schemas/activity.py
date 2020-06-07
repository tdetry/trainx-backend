from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ActivityBase(BaseModel):
    external_id: Optional[str]
    name: Optional[str] = None
    description: Optional[str] = None
    activity_type: Optional[str] = None
    distance: Optional[float] = None
    moving_time: Optional[int]
    elapsed_time: Optional[int]
    total_elevation_gain: Optional[float] = None
    elev_high: Optional[float] = None
    elev_low: Optional[float] = None
    start_date: Optional[datetime] = None
    start_date_local: Optional[datetime] = None
    achievement_count: Optional[int]
    kudos_count: Optional[int]
    comment_count: Optional[int]
    athlete_count: Optional[int]
    workout_type: Optional[int]
    average_speed: Optional[float] = None
    max_speed: Optional[float] = None
    has_kudoed: Optional[bool] = False
    kilojoules: Optional[float] = None
    average_watts: Optional[float] = None
    device_watts: Optional[bool] = False
    calories: Optional[float] = None
    device_name: Optional[float] = None


# Properties to receive on item creation
class ActivityCreate(ActivityBase):
    name: str
    distance: float

    # TODO: determine mandatory


class ActivityInDBBase(ActivityBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Activity(ActivityInDBBase):
    pass


class ActivityInDB(ActivityInDBBase):
    pass
