from database import Base
from sqlalchemy import Column, LargeBinary, Integer


class APIAccess(Base):
    __tablename__ = 'api_access'
    id = Column(Integer, primary_key=True)
    key_hash = Column(LargeBinary)

    def __init__(self, key_hash):
        self.key_hash = key_hash
