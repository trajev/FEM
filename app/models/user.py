from app.db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.mixins import TimestampMixin

class User(TimestampMixin, Base):
  __tablename__="users"
  id:Mapped[int] = mapped_column( primary_key=True )
  name:Mapped[str] = mapped_column( String(50)  )
  email:Mapped[str] = mapped_column( String(100), unique=True )
