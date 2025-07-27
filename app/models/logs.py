from sqlalchemy import Column, Integer, DateTime, String, func, ForeignKey

from app.database.session import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(String, nullable=False)  # e.g., "info", "error", "debug"
    method_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    log = Column(String, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Log (id={self.id}, user_id={self.user_id}, action={self.action}, timestamp={self.timestamp})>"