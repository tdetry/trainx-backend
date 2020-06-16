from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class ExternalUser(Base):
    __tablename__ = 'external_user'
    id = Column(Integer, primary_key=True, index=True)
    external_user_id = Column(String, unique=True, nullable=False, index=True)
    external_source = Column(String, unique=True, nullable=False, index=True)

    full_name = Column(String)
    external_user_access_token = Column(String)
    external_user_refresh_token = Column(String)
    external_user_access_token_expires_at = Column(DateTime)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="external_user")
