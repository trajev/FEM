from app.db.base import Base
import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.user import User
from app.models.mixins import TimestampMixin


class House(TimestampMixin,Base):
  __tablename__="houses"
  id:Mapped[uuid.UUID] = mapped_column( primary_key=True, default=uuid.uuid4  )
  name:Mapped[str] = mapped_column( String(30), nullable=False )
  description:Mapped[str] = mapped_column(String(200), nullable=True)
  currency:Mapped[str] = mapped_column( String(3), default="INR", server_default="INR" )
  join_code:Mapped[str] = mapped_column( String(10), unique=True, index=True, nullable=False )
  created_by:Mapped[uuid.UUID] = mapped_column( ForeignKey("users.id"), nullable=False )
  creator:Mapped[User] = relationship()

