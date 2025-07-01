from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomFacilitiesOrm(Base):
    __tablename__ = 'room_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    rooms_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facilities_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))