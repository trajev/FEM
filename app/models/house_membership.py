from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timezone
from app.models.user import User
from app.models.house import House


class HouseMembership(Base):
  __tablename__="house_memberships"
  id:Mapped[int] = mapped_column( primary_key=True )
  user_id:Mapped[int] = mapped_column( ForeignKey("users.id"), unique=True, nullable=False )
  house_id:Mapped[int] = mapped_column( ForeignKey("houses.id"), nullable=False )
  role:Mapped[str] = mapped_column( default="member", nullable=False )
  joined_at:Mapped[datetime] = mapped_column(  DateTime(timezone=True), default=lambda: datetime.now(timezone.UTC), nullable=False   )
  user:Mapped[User] = relationship()
  house:Mapped[House] = relationship()