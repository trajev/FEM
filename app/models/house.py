from app.db.base import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.user import User
from app.models.mixins import TimestampMixin


class House(TimestampMixin,Base):
  __tablename__="houses"
  id:Mapped[int] = mapped_column( primary_key=True )
  name:Mapped[str] = mapped_column( nullable=False )
  created_by:Mapped[int] = mapped_column( ForeignKey("users.id"), nullable=False )
  creator:Mapped[User] = relationship()

