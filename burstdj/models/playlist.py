from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.types import DateTime
from sqlalchemy.types import String

from burstdj.models import Base
from burstdj.models import types
from burstdj.models.user import User

class Playlist(Base):
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime, server_default=func.now())
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    tracks = Column(types.JSONValue)