from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy.types import DateTime
from sqlalchemy.types import String

from burstdj.models import Base
from burstdj.models import types


class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, server_default=func.now())
    name = Column(String)
    artist = Column(String)
    provider = Column(Integer)
    track_provider_id = Column(String)
    length = Column(Integer)

Index('track_id', Track.provider, Track.track_provider_id, unique=True)