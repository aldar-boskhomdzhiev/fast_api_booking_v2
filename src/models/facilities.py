from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base
from src.models.rooms import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="room_facilities",
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = 'room_facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    rooms_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facilities_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))