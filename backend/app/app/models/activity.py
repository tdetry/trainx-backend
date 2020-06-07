from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Activity(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner = relationship("User", back_populates="activities")
    owner_id = Column(Integer, ForeignKey("user.id"))
    external_id = Column(String)
    name = Column(String)
    description = Column(String)
    activity_type = Column(String)
    distance = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    total_elevation_gain = Column(Float)
    elev_high = Column(Float)
    elev_low = Column(Float)
    start_date = Column(DateTime)
    start_date_local = Column(DateTime)
    achievement_count = Column(Integer)
    kudos_count = Column(Integer)
    comment_count = Column(Integer)
    athlete_count = Column(Integer)
    workout_type = Column(Integer)
    average_speed = Column(Float)
    max_speed = Column(Float)
    has_kudoed = Column(Boolean)
    kilojoules = Column(Float)
    average_watts = Column(Float)
    device_watts = Column(Boolean)
    calories = Column(Float)
    device_name = Column(String)

# TODO: lap and efforts
