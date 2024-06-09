from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import text

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable = False)
    email = Column(String, nullable = False, unique = True)
    phone = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

    def __repr__(self):
        return f"<User(id = {self.id}, username = {self.username}, email = {self.email})>, phone = {self.phone}"