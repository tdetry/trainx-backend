from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class Activity(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
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
    device_name: Optional[str] = None
